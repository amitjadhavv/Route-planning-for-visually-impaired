import os
from torchvision import transforms
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import torch
import torchvision.models as models
import torchvision.models.segmentation as segmentation


root = '.'
image_dir = '/leftImg8bit_trainvaltest/leftImg8bit/train/aachen'  # Update this path
mask_dir = '/gtFine_trainvaltest/gtFine/train/aachen'  
class CustomDataset(Dataset):
    def __init__(self, root, img_dir, mask_dir, transform=None):
        self.root = root
        self.img_dir = os.path.join(root, img_dir)
        self.mask_dir = os.path.join(root, mask_dir)
        self.transform = transform
        self.images = sorted(os.listdir(self.img_dir))

    def __getitem__(self, index):
        img_path = os.path.join(self.img_dir, self.images[index])
        mask_path = os.path.join(self.mask_dir, self.images[index].replace('_leftImg8bit.png', '_gtFine_labelIds.png'))
        
        image = Image.open(img_path).convert("RGB")
        mask = Image.open(mask_path).convert("L")

        if self.transform is not None:
            image = self.transform(image)
            mask = self.transform(mask)

        return {'image': image, 'mask': mask}

    def __len__(self):
        return len(self.images)

# Transformations (if any)
transform = transforms.Compose([
    transforms.Resize((256,256)),
    #transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    # Add any other transformations you need
])

# Create the dataset and data loader
dataset = CustomDataset(root, image_dir, mask_dir, transform)
data_loader = DataLoader(dataset, batch_size=16, shuffle=True)


# Load pre-trained ResNet-34
resnet34 = models.resnet34(pretrained=True)

# Create a DeepLabv3+ model with ResNet-34 as the backbone
deeplab_model = segmentation.deeplabv3_resnet50(pretrained=False, num_classes=30)


import torch.nn as nn
import torch.optim as optim

from torchmetrics.classification import MulticlassJaccardIndex as IoULoss

#os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:256"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.cuda.empty_cache()

num_classes = 30  # Assuming binary segmentation (sidewalk or not)
#batch_size = 5
learning_rate = 0.001
num_epochs = 10

criterion = IoULoss(num_classes = 30).to(device)#nn.CrossEntropyLoss()
optimizer = optim.Adam(deeplab_model.parameters(), lr=learning_rate)


# Rest of your code remains unchanged...

# Move the model to the GPU
deeplab_model = deeplab_model.to(device)
 
# Training loop
for epoch in range(num_epochs):
    deeplab_model.train()
    for batch in data_loader:
        images = batch['image']
        masks = batch['mask']
        #if torch.cuda.is_available():
        images, masks = images.to(device), masks.to(device)
        optimizer.zero_grad()
        #print(images.shape)
        outputs = deeplab_model(images)
        
        masks = masks.squeeze(1)  # Assuming masks have shape (batch_size, 1, height, width)

        # Ensure that masks are of type Long (for class indices)
        #masks = masks.long()
        masks = masks.long()
        #loss = criterion(logits_flat, masks_flat)
        #print(outputs['out'].shape, masks.shape
        #masks = masks.to(device).requires_grad_()
        #print(outputs['out'].requires_grad,masks.requires_grad)
        loss = criterion(outputs['out'], masks)  # Assuming 'out' is the output for segmentation
        loss.requires_grad = True
        loss.backward()
        optimizer.step()

    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item()}')

# Save the trained model

torch.save(deeplab_model.state_dict(), 'deeplab_model.pth')