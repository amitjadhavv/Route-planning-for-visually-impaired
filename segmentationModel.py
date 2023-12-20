import os
from torchvision import transforms
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import torch
import torchvision.models as models
import torchvision.models.segmentation as segmentation


import torch.nn as nn
import torch.optim as optim

from torchmetrics.classification import MulticlassJaccardIndex as IoULoss

root = '.'
image_dir = '/leftImg8bit_trainvaltest/leftImg8bit/train' 
mask_dir = 'gtFine_trainvaltest/gtFine/train'  


# Transformations (if any)
transform = transforms.Compose([
    transforms.Resize((256,256)),
    transforms.ToTensor(),
])

class CustomDataset(Dataset):
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
        if self.transform is not None:
            image = self.transform(image)
            mask = self.transform(mask)

        return {'image':image, 'mask':mask}

    def __len__(self):
        return len(self.images)


dataset = CustomDataset(root, image_dir, mask_dir, transform)
data_loader = DataLoader(dataset, batch_size=16, shuffle=True)


# Load pre-trained ResNet-34
resnet34 = models.resnet34(pretrained=True)

# Create a DeepLabv3+ model with ResNet-34 as the backbone
deeplab_model = segmentation.deeplabv3_resnet50(pretrained=False, num_classes=30)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.cuda.empty_cache()

num_classes = 30 
learning_rate = 0.001
num_epochs = 10

criterion = IoULoss(num_classes = 30).to(device)
optimizer = optim.Adam(deeplab_model.parameters(), lr=learning_rate)


deeplab_model = deeplab_model.to(device)

for epoch in range(num_epochs):
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

    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item()}')


torch.save(deeplab_model.state_dict(), 'deeplab_model.pth')