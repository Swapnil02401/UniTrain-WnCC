import torch
import torch.nn as nn
import torchvision.models as models

# Define the ResNet-9 model in a single class
class ResNet9(nn.Module):
    def __init__(self, num_classes):
        super(ResNet9, self).__init__()
        self.in_channels = 64

        # Initial convolution layer
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)

        # Residual blocks
        self.layer1 = self.make_layer(64, 2, stride=1)
        self.layer2 = self.make_layer(128, 2, stride=2)
        self.layer3 = self.make_layer(256, 2, stride=2)
        self.layer4 = self.make_layer(512, 2, stride=2)

        # Global average pooling and fully connected layer
        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, num_classes)

    def make_layer(self, out_channels, num_blocks, stride):
        layers = []
        layers.append(self.build_residual_block(self.in_channels, out_channels, stride))
        self.in_channels = out_channels
        for _ in range(1, num_blocks):
            layers.append(self.build_residual_block(self.in_channels, out_channels, stride=1))
        return nn.Sequential(*layers)

    def build_residual_block(self, in_channels, out_channels, stride):
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
        )

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.avg_pool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)

 #ResNet50 functionality addition       
class ResNet9_50(nn.Module):
    def __init__(self, num_classes):
        super(ResNet9_50, self).__init__()
        
        self.resnet9 = ResNet9(num_classes)
        self.resnet50 = models.resnet50(pretrained=True)

    def forward(self, x):
         x = self.resnet50(x)
#GoogLeNet functionality addition
import torch
import torch.nn as nn
import torchvision.models as models

class GoogleNetModel(nn.Module):
    def __init__(self, num_classes):
        super(GoogleNetModel, self).__init()
        
        # Load the pre-trained GoogleNet model
        self.googlenet = models.inception_v3(pretrained=True)
        
        # Modify the classification head to match the number of classes in your dataset
        num_ftrs = self.googlenet.fc.in_features
        self.googlenet.fc = nn.Linear(num_ftrs, num_classes)

    def forward(self, x):
        # Pass input through the GoogleNet model
        x1 = self.googlenet(x)
        x2 = self.resnet50(x)
        x3 = self.resnet9(x)
        x = x1 + x2 + x3
        return x


