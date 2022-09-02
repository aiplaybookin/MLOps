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
import time

#logger = logging.getLogger('timm.models')
#logger.disabled=True
#logger.propogate = False

@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg : DictConfig) -> None:

    # Get Label
    label_link = "https://storage.googleapis.com/bit_models/ilsvrc2012_wordnet_lemmas.txt"
    LABELS = requests.get(label_link).text.strip().split('\n')
    #print('1st-line')
    # Get Image 
    image_link = cfg.db.IMAGE
    #"https://github.com/pytorch/hub/raw/master/images/dog.jpg" "https://pbs.twimg.com/profile_images/664169149002874880/z1fmxo00_400x400.jpg"
    urllib.request.urlretrieve(image_link, "sample.png")
    img = Image.open("sample.png")
    for a,b in logging.Logger.manager.loggerDict.items():
        b.disabled=True

    #logger = logging.getLogger('my-logger')
    #logging.basicConfig(level=logging.CRITICAL)
    #logger.disabled=True
    #logger.propogate = False
    # Get Model
    m = timm.create_model(cfg.db.MODEL, pretrained=True)
    #print('wgy?')
    #logger.disabled = False
    #logger.propogate = True
    # To put the model into inference mode, 
    # as operators such as dropout and batchnorm behave differently depending on the mode

    transform = create_transform(
        **resolve_data_config({}, model=m)
    )
    m.eval()
    
    img = img.convert('RGB')
    img = transform(img).unsqueeze(0)
    #print(img)

    with torch.no_grad():
        out=m(img)

    probabilities = torch.nn.functional.softmax(out[0], dim=0)
    values, indices = torch.topk(probabilities, k=1)

    x= {LABELS[i]: v.item() for i,v in zip(indices, values)}
    #print(x)
    
    # Serializing json
    json_object = json.dumps(x)
    print(json_object)
    #Writing to sample.json
    with open("inference.json", "w") as outfile:
        outfile.write(json_object)
    
    return(json_object)

if __name__ == "__main__":
    #logger = logging.getLogger('timm.models')
    #logger.setLevel(logging.CRITICAL)
    #logger.disabled=True
    for a,b in logging.Logger.manager.loggerDict.items():
        b.disabled=True
    my_app()