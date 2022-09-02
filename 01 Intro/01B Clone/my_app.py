import torch
import timm
import PIL
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform 
import requests
import urllib.request 
from PIL import Image
import numpy as np
import hydra
from omegaconf import DictConfig, OmegaConf
import json
import logging

@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg : DictConfig) -> None:

    # Get Label
    label_link = "https://storage.googleapis.com/bit_models/ilsvrc2012_wordnet_lemmas.txt"
    LABELS = requests.get(label_link).text.strip().split('\n')

    # Get Image 
    image_link = cfg.db.IMAGE

    urllib.request.urlretrieve(image_link, "sample.png")
    img = Image.open("sample.png")

    for a,b in logging.Logger.manager.loggerDict.items():
        #print(a,b)
        b.disabled=True

    # Get Model
    m = timm.create_model(cfg.db.MODEL, pretrained=True)

    transform = create_transform(
        **resolve_data_config({}, model=m)
    )
    m.eval()
    
    img = img.convert('RGB')
    img = transform(img).unsqueeze(0)
    
    with torch.no_grad():
        out=m(img)

    probabilities = torch.nn.functional.softmax(out[0], dim=0)
    values, indices = torch.topk(probabilities, k=1)

    x= {LABELS[i]: v.item() for i,v in zip(indices, values)}
    
    # Serializing json
    json_object = json.dumps(x)
    print(json_object)
    
    #Writing to sample.json
    #with open("inference.json", "w") as outfile:
    #    outfile.write(json_object)
    
    return(json_object)

if __name__ == "__main__":
    my_app()