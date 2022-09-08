1. Clone https://github.com/ashleve/lightning-hydra-template

2. Include COG into this for inference only (image)

3. Add CIFAR10 datamodule (see how MNIST is integrated with the template, and similarly integrate CIFAR10)

4. Refer to this if you need help with CIFAR10: 

    4a. https://colab.research.google.com/drive/1dnc5jVmCLN1UsSL_p4X9UNgE77Y6UpoD?usp=sharing, (Links to an external site.)  

    4b. https://juliusruseckas.github.io/ml/lightning.html (Links to an external site.) , 

    4c. https://pytorch-lightning.readthedocs.io/en/stable/notebooks/lightning_examples/cifar10-baseline.html (Links to an external site.) see create_model call, and use timm pretrained model there.

5. It should include a Makefile for building the docker make build should build the docker image

6. Include scripts train.py and eval.py for training and eval(metrics) for the model, docker run <image>:<>tag python3 src/train.py experiment=experiment_name.yaml

7. Push the changes in a repo and share link for it. NOTE: there are github actions included that will run automatically on push.


Add ```Dockerfile```

Update the Makefile, add -
```
build: ## Building the docker image
	@echo Build docker image.....
	@docker build -t testimg .
```

Run below command in terminal to create a docker image
```
make build
```

To launch docker container for training ( docker image named testimg got created from above build command mentioned in MAKEFILE) 
```
docker run --rm testimg src/train.py
```

To perform evaluation from previously trained and saved model checkpoint 
```
docker run --rm testimg src/eval.py ckpt_path=logs/train/runs/2022-09-08_09-36-23/checkpoints/last.ckpt
```