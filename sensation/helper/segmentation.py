import torch.nn as nn
import segmentation_models_pytorch as smp
import torchvision.models.segmentation as segmentation

class DeepLabV3PResNet50(nn.Module):
    def __init__(self, num_classes: int = 8):
        super(DeepLabV3PResNet50, self).__init__()
        self.layer = segmentation.deeplabv3_resnet50(pretrained=False, num_classes=8)
        self.activation = nn.Sigmoid()
        self.n_classes = num_classes

    def forward(self, x):
        return self.layer(x)
