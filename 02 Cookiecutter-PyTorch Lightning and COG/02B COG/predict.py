from typing import Any
from cog import BasePredictor, Input, Path

import json
import torch
import timm
import numpy as np

from timm.data.transforms_factory import transforms_imagenet_eval

from PIL import Image

class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory to make running multiple predictions efficient"""
        self.model = timm.create_model('efficientnet_b3a', pretrained=True)
        self.model.eval()
        self.transform = transforms_imagenet_eval()

        with open("imagenet_1k.json", "r") as f:
            self.labels = list(json.load(f).values())

    # Define the arguments and types the model takes as input
    def predict(self, image: Path = Input(description="Image to classify")) -> Any:
        """Run a single prediction on the model"""
        # Preprocess the image
        img = Image.open(image).convert('RGB')
        img = self.transform(img)

        # Run the prediction
        with torch.no_grad():
            labels = self.model(img[None, ...])
            labels = labels[0] # we'll only do this for one image

        # top 5 preds
        topk = labels.topk(5)[1]
        output = {
            # "labels": labels.cpu().numpy(),
            "topk": [self.labels[x] for x in topk.cpu().numpy().tolist()],
        }

        return output