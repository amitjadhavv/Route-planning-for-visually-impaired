import logging
import os
from torchvision import transforms
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import torch
import torchvision.models as models
import torchvision.models.segmentation as segmentation
from utils import get_logger
from datetime import date
import torch.multiprocessing as mp
import random

import torch.nn as nn
import torch.optim as optim

from torchmetrics.classification import MulticlassJaccardIndex as IoULoss

root = r'path\to\your\director'
image_dir = r'leftImg8bit_trainvaltest\leftImg8bit\train'
mask_dir = r'gtFine_trainvaltest\gtFine\train'
checkpoints_dir = r'checkpoints\deeplab_model.pth'
logger_dir = 'exp\\'


transform = transforms.Compose([
    transforms.Resize((256,256)),
    transforms.ToTensor(),
])

class CustomDataset(Dataset):
    def __init__(self, root,img_dir, mask_dir, transform=None):
        self.root = root
        self.img_dir = os.path.join(root ,img_dir)
        self.mask_dir = os.path.join(root,mask_dir)
        self.city_dir = os.listdir(self.img_dir)
        
        self.transform = transform
        self.images = []
        self.masks = []
        # TODO delete it
        city_list = random.sample(self.city_dir,3)
        current_date = str(date.today())
        logger_file = 'exp_' + current_date + '.log'
        logger = get_logger(logger_dir,logger_file)
        logger.info(f'get model trained on city list [' + str(city_list) + ']')
        for city in city_list:
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


def train(model,data_loader,optimizer,criterion,hyper_params):
    current_date = str(date.today())
    logger_file = 'exp_' + current_date + '.log'
    logger = get_logger(logger_dir,logger_file)
    process_id = os.getpid()
    logging.info(f'''Process-{process_id}  Starting training:
            Epochs:          {hyper_params["Epochs"]}
            Batch size:      {hyper_params["Batch_size"]}
            Learning rate:   {hyper_params["Learning_rate"]}
            Training size:   {hyper_params["Training_size"]}
            Device:          {hyper_params["Device"]}
            Loss type:       {hyper_params["Loss_type"]}
            Backbone:        {hyper_params["Backbone"]}
        ''')
    for epoch in range(hyper_params["Epochs"]):
        model.train()
        for batch_i, batch in enumerate(data_loader):
            images = batch['image']
            masks = batch['mask']
            images, masks = images.to(hyper_params["Device"]), masks.to(hyper_params["Device"])
            optimizer.zero_grad()
            outputs = model(images)

            masks = masks.squeeze(1)
            masks = masks.long()

            loss = criterion(outputs['out'], masks)
            loss.requires_grad = True
            loss.backward()
            optimizer.step()
            logger.info(f'Process-{process_id} Epoch [{epoch + 1}/{hyper_params["Epochs"]}],Batch_i: {batch_i} Loss: {loss.item()}')



if __name__ == '__main__':

    batch_size = 8
    num_classes = 19
    learning_rate = 0.001
    num_epochs = 10
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    loss_type = 'IoU'
    backbone = 'resnet50'
    load_checkpoints = False

    dataset = CustomDataset(root, image_dir, mask_dir, transform)
    train_size = len(dataset)
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True,num_workers=4)



    # Load pre-trained ResNet-34
    resnet34 = models.resnet34(pretrained=True)

    # Create a DeepLabv3+ model with ResNet-34 as the backbone
    deeplab_model = segmentation.deeplabv3_resnet50(pretrained=False, num_classes=19)
    if load_checkpoints:
        deeplab_model.load_state_dict(torch.load(checkpoints_dir))
    deeplab_model.share_memory()



    torch.cuda.empty_cache()
    cuda0 = torch.device('cuda:0')
    cuda1 = torch.device('cuda:1')



    criterion = IoULoss(num_classes = 19).to(device)

    optimizer = optim.Adam(deeplab_model.parameters(), lr=learning_rate)


    deeplab_model = deeplab_model.to(device)



    hyper_params = {
        "Epochs": num_epochs,
        "Batch_size":      batch_size,
        "Learning_rate": learning_rate,
        "Training_size": train_size,
        "Device": device,
        "Loss_type": loss_type,
        "Backbone": backbone,
    }

    processes = []
    num_processes = 2
    for i in range(num_processes):  # No. of processes
        p = mp.Process(target=train, args=(deeplab_model,data_loader,optimizer,criterion,hyper_params))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    torch.save(deeplab_model.state_dict(), 'deeplab_model.pth')