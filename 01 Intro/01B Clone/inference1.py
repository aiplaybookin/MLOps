import timm 
import urllib.request 
from PIL import Image
import numpy as np


# Get Image 
image_link = "https://github.com/pytorch/hub/raw/master/images/dog.jpg" #"https://i.imgur.com/ExdKOOz.png"

urllib.request.urlretrieve(image_link, "sample.png")
img = Image.open("sample.png")

# Get Model
model_name = 'mobilenetv3_large_100'

m = timm.create_model(model_name, pretrained=True)
# It is important to call model.eval() before exporting the model, to put the model into inference mode, 
# as operators such as dropout and batchnorm behave differently depending on the mode
m=m.cpu()
m.eval()

from timm.data import ImageDataset, create_loader, resolve_data_config

loader = create_loader(
        ImageDataset('./results'),
        input_size=None, #config['input_size'],
        batch_size=10, #args.batch_size,
        #use_prefetcher=True,
        #interpolation=config['interpolation'],
        #mean=config['mean'],
        #std=config['std'],
        #num_workers=args.workers,
        crop_pct=1.0 #if test_time_pool else config['crop_pct']
        )


#-----
img = torch.as_tensor(np.array(img, dtype=np.float32)).transpose(2,0)[None]
