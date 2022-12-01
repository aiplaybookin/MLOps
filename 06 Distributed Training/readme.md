# Distributed Training

## Need
- Faster training
- Acccomodate large models like GPT ( different parts are trained on different machines)

Training in multiple GPUs has 2 assets -

- Model
- Data 

Both has to be distrbuted somehow across multiple GPUs. There are 2 ways

1. Data Parallel (DP)
2. Distributed Data Parallel (DDP)

Similar to parallel/distributed computing, multi thread -> Master-Worker

## Multi GPU Training

Pytorch provides two settings for distributed training: 
 - torch.nn.DataParallel (DP) and 
 - torch.nn.parallel.DistributedDataParallel (DDP)
 
 where the latter is officially recommended. In short, DDP is faster, more flexible than DP.


[DataParallel](https://pytorch.org/docs/stable/generated/torch.nn.DataParallel.html#torch.nn.DataParallel)

<img src="images/1-shared-model.png" />
Shared model

Pytorch implementation. [Read more](https://pytorch.org/docs/stable/nn.html#module-torch.nn.parallel)

DP *splits a batch across k GPUs*. That is, if you have a batch of 32 and use DP with 2 gpus, each GPU will process 16 samples, after which the root node will aggregate the results.

#### *Weights are averaged and send to all GPUs in order to sync the model. Gradients unctouched at master during model sync.*

```
from torch.nn import DataParallel as DP

wrapped_model = DP(model)
```

[Distributed Data Parallel](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html?highlight=distributed)

#### *The fundamental thing DDP does is to copy the model to multiple gpus, gather the gradients from them, average the gradients to update the model, then synchronize the model over all K processes* GPU 0 only uses optimiser over the gradients!

DP accumulates gradients to the same ```.grad``` field, while DDP first use ```all_reduce``` to calculate the gradient sum across all processes and divide that by ```world_size``` to compute the mean.

<img src="images/2-distributed-dataparallel.png" />

- Each GPU across each node gets its own process.
- Each GPU gets visibility into a subset of the overall dataset. It will only ever see that subset.
- Each process inits the model.
- Each process performs a full forward and backward pass in parallel.
- The gradients are synced and averaged across all processes.
- Each process updates its optimizer.

```
from torch.nn.parallel import DistributedDataParallel as DDP

wrapped_model = DDP(model)
```

[Design : How are Gradients applied in backward process?](https://pytorch.org/docs/stable/notes/ddp.html)

*May need to see latest link for designs

<img src="images/3-all-reduce-1.png" />
<img src="images/4-all-reduce-2.png" />

## DistributedSampler

https://pytorch.org/docs/stable/data.html#torch.utils.data.distributed.DistributedSampler

Useful ```in conjunction with torch.nn.parallel.DistributedDataParallel```. In such a case, each process can pass a DistributedSampler instance as a DataLoader sampler, and load a subset of the original dataset that is *exclusive to it*.

The ```DistributedSampler``` simply subsamples the data among the whole dataset.

[Code](https://github.com/pytorch/pytorch/blob/master/torch/utils/data/distributed.py#L68)

```
# subsample
indices = indices[self.rank:self.total_size:self.num_replicas]
```

#### with PyTorch Lightning

No code changes, just add the GPU ids you want to train on

```Trainer(gpus=[0, 1])```

https://pytorch-lightning.readthedocs.io/en/1.4.0/advanced/multi_gpu.html

### Logging

Wherever doing ```self.log``` use ```sync_dist=True``` otherwise you will have metric from the master node using a portion of data during multi gpu training.

```
# Add sync_dist=True to sync logging across all GPU workers
self.log('validation_loss', loss, on_step=True, on_epoch=True, sync_dist=True)
```

### Distributed Backends

GLOO and NCCL

- This is primarily used when there’s need for multiple GPUs communication or multi-node multi-gpu communication.

- There are other options like MPI, but NCCL performs far better than it when it comes to GPU Clusters.

- In synchronized data-parallel distributed deep learning, the major computation steps are:

    1. Compute the gradient of the loss function using a minibatch on each GPU.
    2. Compute the mean of the gradients by inter-GPU communication.
    3. Update the model.

NCCL from Nvidia is best as of now!

[More on the All Reduce Algorithm here](https://tech.preferred.jp/en/blog/technologies-behind-distributed-deep-learning-allreduce/)



#### #Workers vrs #GPUs

Workers are based on #CPUs , reads data and creates batch. *Pefer to have 2 workers per GPU.* or N cores then N workers.

GPU compute will be fast and may wait for batch data.


### Request Service Quotas
We may not have access to GPUs Spot instance, then we must request for them (this is once)

1. Go to Service Quotas -> AWS Services 

2. Search for Amazon Elastic Compute Cloud (Amazon EC2) and click on it

3. Select instance types which you need (here I am selecting G&VT type). Click request quota increase and specify the maximum number of vCPUs for all running or requested G and VT Spot Instances per Region. (e.g. I selected 64 - could use 4*16).

<img src="images/service_quota.png" />

### EC2 Spot Instance (How do we know Spot Instance Availability?)

1. Go to EC2 -> (left sidebar) Spot Requests -> Request Spot Instances 

2. Scroll down Instance Type Requirements -> select Manual -> Add Instances if not in list below 



### Launch an EC2 Instance

ssh from local
```
ssh -i <>.pem ubuntu@<Public IP of EC2>
```

From Local get your public keys (use ```ssh-keygen```, if not available)
```
cat ~/.ssh/id_rsa.pub
```

In EC2 instance
```
vim ~/.ssh/authourized_keys
```

#### When wish to copy from one instance to another

1. Copy and paste public keys from small instance to gpu instance to fetch the code
2.  

rsync -r --info=progress2 lightning-hydra-template ubuntu@<Public IP of GPU>:~/


### Run in 1 GPU instance 
e.g. ```g4dn.xlarge```

1. Launch the instance 

2. List the environments available and go to pytorch one

```
conda env list
source activate pytorch
```
3. Git clone the repo
```
git clone https://github.com/aiplaybookin/lightning-hydra-template.git
```

4. Change the config->experiment->cifar.yaml : ```- override /trainer: gpu.yaml```

5. Change the config->datamodule->cifar10.yaml : ```num_workers: 4```




Run nvidia smi every 0.5 sec ```watch -n 0.5 nvidia-smi``` 

Kill a previous orphan process, go check
```ps -ef | grep python``` and ```nvidia-smi``` later 

```kill -9 <PID>```


Ray : 
Create instance , yaml file for aws for instances. setup iam roles, copy code , 

slurm 

## Others

- Generally set 2 workers per CPU, so that we have better utilization to create batch and fed to GPUs. GPU might process faster than CPU.

# Steps : -

1. Lanch EC2 instance

2. Name multi-gpu-training

3. OS image ```Ubuntu``` Deep Learning AMI GPU Pythorch 1.12.1

4. Instance Type (choose from acclerated compute, eg. )

```g4dn.xlarge```

5. Select the existing kep pair (or create and save a new one)

6. Security group - existing one (or create one)

7. Storage - minimum gb will show up, we will keep as is.

8. Click on Advance & Select ```Request Spot Instances```

9. Launch!

10. Local machine terminal do ssh ```ssh -i file.pem ubuntu@<ip address>```

11. Get code from git 
```
git clone https://github.com/aiplaybookin/lightning-hydra-template.git
```

13. Deep learning Pytorch Ubuntu image comes with pytorch venv. Check the env list and use pytorch one.
```
conda env list

source activate pytorch
```
May be check version of pytorch

14. Go to the cloned folder and install the packages from requirements.txt
```
pip install -r requirements.txt
```

15. 

### For single node GPU Training

a. Change the config->experiment->cifar.yaml : ```- override /trainer: gpu.yaml```. Specify devices in gpu.yaml as per the gpus available.

b. Change the config->datamodule->cifar10.yaml : ```num_workers: 4``` . (as per number of cpus)

c. Run training ```python3 src/train.py experiment=cifar```

### For DDP GPU Training

Change config->experiment->cifar.yaml : ```- override /trainer: ddp.yaml```

Change the config->datamodule->cifar10.yaml : ```num_workers: 4``` 
Change the config->trainer->ddp.yaml : ```devices: 1``` as i had only 1 gpu per instance


python3 src/train.py experiment=cifar trainer.default_root_dir=$(date +%Y-%m-%d_%H-%M-%S) callbacks.model_checkpoint.dirpath=logs/train/runs 


### For Multi node Multi GPU training

A1. Create multi node instances say 2, eacg ```g4dn.xlarge``` (See step above, just need to add 2 or more instances)

Security group should have -
```Type: Custom TCP```     ```Port range : 1000-65535``` for communication between nodes

SSH from local machine

source activate pytorch

Install tmux
```
cd
git clone https://github.com/gpakosz/.tmux.git
ln -s -f .tmux/.tmux.conf
cp .tmux/.tmux.conf.local .
```

Create tmux session
```
tmux new -s work
```

Clone the repo in both
```
git clone https://github.com/aiplaybookin/lightning-hydra-template.git
```

cd lightning-hydra-template

pip install -r requirements.txt

When logging on epoch level in distributed setting to accumulate the metric across devices. e.g. 
self.log('train/acc', ..., ```sync_dist=True```)

NOTE : Both should have same code /files

change the batch size to 256

change min/ max epoch to 

logger=tensorboard

Comment code for test in node num >0



Master Node, can change port and try. Private IP addr

Use ```hostname``` to get Private IPv4 addresses 
```
MASTER_PORT=29500 MASTER_ADDR=<Private IPv4 addresses> WORLD_SIZE=2 NODE_RANK=0 python src/train.py trainer=ddp trainer.devices=1 trainer.num_nodes=2
```

MASTER_PORT=29500 MASTER_ADDR=172.31.31.106 WORLD_SIZE=2 NODE_RANK=0 python src/train.py trainer=ddp trainer.devices=1 trainer.num_nodes=2 trainer.default_root_dir=$(date +%Y-%m-%d_%H-%M-%S) callbacks.model_checkpoint.dirpath=logs/train/runs 

MASTER_PORT=29500 MASTER_ADDR=172.31.31.106 WORLD_SIZE=2 NODE_RANK=1 python src/train.py trainer=ddp trainer.devices=1 trainer.num_nodes=2 trainer.default_root_dir=$(date +%Y-%m-%d_%H-%M-%S) callbacks.model_checkpoint.dirpath=logs/train/runs 

trainer.max_epochs=2

MASTER_PORT=29500 MASTER_ADDR=172.31.47.238 WORLD_SIZE=2 NODE_RANK=0 python src/train.py trainer=ddp trainer.devices=1 trainer.max_epochs=2 trainer.num_nodes=2 trainer.default_root_dir=$(date +%Y-%m-%d_%H-%M-%S) callbacks.model_checkpoint.dirpath=logs/train/runs 

MASTER_PORT=29500 MASTER_ADDR=172.31.47.238 WORLD_SIZE=2 NODE_RANK=1 python src/train.py trainer=ddp trainer.devices=1 trainer.max_epochs=2 trainer.num_nodes=2 trainer.default_root_dir=$(date +%Y-%m-%d_%H-%M-%S) callbacks.model_checkpoint.dirpath=logs/train/runs

While Running epoch Output can be seen on master node

Use tmux sessions
[Refer](https://github.com/aiplaybookin/MLOps/tree/main/05%20AWS%20Deployment#TMUX)



- Increase the batch size (highest batch_size possible for both strategies)
- Change the model name to "vit_base_patch32_224"
- Store best checkpoint of both to AWS S3




World size = num of GPUs x number of nodes

Same seed should be used in all nodes


Run nvidia smi every 0.5 sec ```watch -n 0.5 nvidia-smi``` 

Kill a previous orphan process, go check
```ps -ef | grep python``` and ```nvidia-smi``` later 

```kill -9 <PID>```


us-east-1

ap-south-1

