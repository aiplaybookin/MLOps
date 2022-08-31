import torch
import timm
import PIL
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform 
import requests
import urllib.request 
from PIL import Image
import numpy as np

# Get Label
label_link = "https://storage.googleapis.com/bit_models/ilsvrc2012_wordnet_lemmas.txt"
LABELS = requests.get(label_link).text.strip().split('\n')

# Get Image 
image_link = "https://github.com/pytorch/hub/raw/master/images/dog.jpg" #"https://i.imgur.com/ExdKOOz.png"
urllib.request.urlretrieve(image_link, "sample.png")
img = Image.open("sample.png")

# Get Model
model_name = 'resnet18'

m = timm.create_model(model_name, pretrained=True)

# To put the model into inference mode, 
# as operators such as dropout and batchnorm behave differently depending on the mode

transform = create_transform(
    **resolve_data_config({}, model=m)
)
m.eval()

def predict_fn(img):

    img = img.convert('RGB')
    img = transform(img).unsqueeze(0)
    #print(img)

    with torch.no_grad():
        out=m(img)

    probabilities = torch.nn.functional.softmax(out[0], dim=0)
    values, indices = torch.topk(probabilities, k=1)

    return({LABELS[i]: v.item() for i,v in zip(indices, values)})

x = predict_fn(img)
print(x)