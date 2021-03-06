from collections import OrderedDict
import torch
from torch import nn
from torchvision import models


def load_model(checkpoint_path):
    model = models.resnet152(pretrained=True)
    classifier = nn.Sequential(OrderedDict([
        ("dropout", nn.Dropout(0.2)),
        ("fc1", nn.Linear(2048, 512)),
        ('batchM1',nn.BatchNorm1d(512)),
        ("relu1", nn.ReLU()),
        ("dropout2", nn.Dropout(0.2)),
        ("fc2", nn.Linear(512, 102)),
        ("output", nn.LogSoftmax(dim=1))
    ]))
    model.fc = classifier
    check_point = torch.load(checkpoint_path, map_location="cpu")
    model.load_state_dict(check_point["state_dict"], strict=False)
    for param in model.parameters():
        param.requires_grad = False
    model.eval()
    return model
# Load your model to this variable
model = load_model('/home/workspace/classifier.pth')
   
# If you used something otherthan 224x224 cropped images, set the correct size here
image_size = 224
# Values you used for normalizing the images. Default here are for 
# pretrained models from torchvision.
norm_mean = [0.485, 0.456, 0.406]
norm_std = [0.229, 0.224, 0.225]
