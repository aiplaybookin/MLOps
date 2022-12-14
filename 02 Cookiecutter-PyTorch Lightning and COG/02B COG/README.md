[cookicutter](https://cookiecutter.readthedocs.io/en/stable/)

Makes very easy to ship ML/DL models to production **by making Dockerfile effortlessly**

cog run actually calls docker run (syntax similar to docker)

1️⃣ Current volume will be mounted automatically to running conatiner

2️⃣ If you specified use cuda or use gpus =true, these gpus are passed to running container

✨ Best Part of COG:  No more CUDA hell. Cog knows which CUDA/cuDNN/PyTorch/Tensorflow/Python combos are compatible and will set it all up correctly for you.

Assuming we have docker ( and Im using gitpod here)
Install
```
sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_`uname -s`_`uname -m`
sudo chmod +x /usr/local/bin/cog
```

## 🚀 Classification model from timm 

1. Create a **cog.yaml** file
```
build:
  python_version: "3.10"
  python_packages:
    - torch==1.12.1
    - torchvision==0.13.1
    - timm==0.6.7
predict: "predict.py:Predictor"
```

2. Make predict.py
3. Placing json file of classes label and ids
4. Get image from internet to make inference
```
IMAGE_URL=https://gist.githubusercontent.com/bfirsh/3c2115692682ae260932a67d93fd94a8/raw/56b19f53f7643bb6c0b822c410c366c3a6244de2/mystery.jpg
curl $IMAGE_URL > input.jpg
```
5. make prediction
```
cog predict -i image=@input.jpg
```
NOTE : The first time you run cog predict, the build process will be triggered to generate a Docker container that can run your model. The next time you run cog predict the pre-built container will be used.

6. Alternatively **better build image first** by (same as docker command, with no dot)-
```
cog build -t <imagename>
```

7. Call for prediction -
```
cog predict <imagename> -i image=@input.jpg
```

8. Generate **Dockerfile** This could also be used as starter dockerfile ( it tries to use multistage docker)
```
cog debug dockerfile > Dockerfile
```


### Reference 
https://github.com/replicate/cog/blob/main/docs/getting-started.md