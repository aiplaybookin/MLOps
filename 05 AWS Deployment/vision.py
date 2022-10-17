import urllib

import gradio as gr
import torch
import timm
import numpy as np

from PIL import Image
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform

from typing import Dict

MODEL: str = "resnet18"

model = timm.create_model(MODEL, pretrained=True)
model.eval()

# Download human-readable labels for ImageNet.
# get the classnames
url, filename = (
    "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt",
    "imagenet_classes.txt",
)
urllib.request.urlretrieve(url, filename)
with open("imagenet_classes.txt", "r") as f:
    categories = [s.strip() for s in f.readlines()]

def predict(inp_img: Image) -> Dict[str, float]:

    # print("input1:", inp_img.size)
    # print("input2:", inp_img2.shape)

    config = resolve_data_config({}, model=MODEL)
    transform = create_transform(**config)

    img_tensor = transform(inp_img).unsqueeze(0)  # transform and add batch dimension

    # inference
    with torch.no_grad():
        out = model(img_tensor)
        probabilities = torch.nn.functional.softmax(out[0], dim=0)
        confidences = {categories[i]: float(probabilities[i]) for i in range(1000)}

    return confidences

if __name__ == "__main__":
    gr.Interface(
        fn=predict, inputs=gr.Image(type="pil"), outputs=gr.Label(num_top_classes=10)
    ).launch(server_name="0.0.0.0")