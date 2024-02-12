import os
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from PIL import Image
import torch.nn as nn
import torch.optim as optim
import torch
import torchvision.models as models
import torchvision.models.segmentation as segmentation
from torchmetrics.classification import MulticlassJaccardIndex as IoULoss
from tqdm import tqdm
from datetime import date
import sys
import numpy as np

labels = [0,7,8,19,20,24,26,33]
nolabels = [x for x in range(-1,34) if x not in labels]

transform = transforms.Compose([
    transforms.Resize((512,256)),
    #transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
])

class CustomDataset(datasets.ImageFolder):
    def __init__(self, root,img_dir, mask_dir, transform=None):
        self.root = root
        self.img_dir = os.path.join(root,img_dir)
        self.mask_dir = os.path.join(root,mask_dir)
        self.city_dir = os.listdir(self.img_dir)
        
        self.transform = transform
        self.images = []
        self.masks = []
        for city in self.city_dir:
            city_img = os.path.join(self.img_dir,city)
            city_mask = os.path.join(self.mask_dir,city)
            
            for file in os.listdir(city_img):
                img_path = os.path.join(city_img,file)
                mask_path = os.path.join(city_mask,file)
                self.images.append(img_path)
                self.masks.append(mask_path)
                
    def __getitem__(self, index):
        img_path = self.images[index]
        mask_path = self.masks[index].replace('_leftImg8bit.png', '_gtFine_labelIds.png')
        image = Image.open(img_path).convert("RGB")
        mask = Image.open(mask_path).convert("L")
        mask = np.array(mask)
	for i in nolabels:
    	    mask[mask == i] = 0
	mask = Image.fromarray(mask)
        if self.transform is not None:
            image = self.transform(image)
            mask = self.transform(mask)

        return {'image':image, 'mask':mask}

    def __len__(self):
        return len(self.images)


root = ''
image_dir = sys.argv[1] #'/kaggle/input/images/leftImg8bit_trainvaltest/leftImg8bit/train' 
mask_dir = sys.argv[2] #'/kaggle/input/image-segmentation/gtFine_trainvaltest/gtFine/train'

val_img = sys.argv[3] #"/kaggle/input/images/leftImg8bit_trainvaltest/leftImg8bit/val"
val_mask = sys.argv[4] #"/kaggle/input/image-segmentation/gtFine_trainvaltest/gtFine/val"

dataset = CustomDataset(root,image_dir, mask_dir, transform)
data_loader = DataLoader(dataset, batch_size=8, shuffle=True)
valdata = CustomDataset(root,val_img,val_mask,transform)
valloader = DataLoader(valdata,batch_size=8,shuffle=True)



# Load pre-trained ResNet-34
resnet34 = models.resnet34(pretrained=True)

# Create a DeepLabv3+ model with ResNet-34 as the backbone
deeplab_model = segmentation.deeplabv3_resnet50(pretrained=False, num_classes=8)


#os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:256"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.cuda.empty_cache()

num_classes = 8
#batch_size = 5
learning_rate = 0.0001
num_epochs = 40

criterion = IoULoss(num_classes = num_classes).to(device)#nn.CrossEntropyLoss()
optimizer = optim.Adam(deeplab_model.parameters(), lr=learning_rate)

#scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

deeplab_model = deeplab_model.to(device)


best_val_loss = float('inf')
# Training loop
for epoch in tqdm(range(num_epochs)):
    deeplab_model.train()
    for batch in data_loader:
        images = batch['image']
        masks = batch['mask']
        images, masks = images.to(device), masks.to(device)
        optimizer.zero_grad()
        outputs = deeplab_model(images)
        masks = masks.squeeze(1)
        masks = masks.long()
        loss = criterion(outputs['out'], masks)
        loss.requires_grad = True
        loss.backward()
        optimizer.step()
    
    deeplab_model.eval()
    total_loss = 0.0
    with torch.no_grad():
        for val_batch in valloader:
            val_images = val_batch['image'].to(device)
            masks = val_batch['mask'].to(device)
            outputs = deeplab_model(val_images)
            masks = masks.squeeze(1)
            masks = masks.long()
            loss = criterion(outputs['out'], masks)
            total_loss += loss.item() * images.size(0)
        avg_val_loss = total_loss / len(valloader.dataset)
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            print(f'Saving the model at Epoch [{epoch + 1}/{num_epochs}]')
            torch.save(deeplab_model.state_dict(), 'deeplab_model.pth')
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item()}, Val Loss: {avg_val_loss}')
