To build the docker

> docker build --tag mnist-hogwild .

To run docker
--rm : Used to remove the docker when docker run is existed

> docker run --rm -it mnist-hogwild


List images

> docker images

Start a container

> docker start compassionate_jepsen

View running container

> docker ps

Get details about a container

> docker inspect <container_name or container_id>

To push to Docker hub repository [ to be usd by other teams/ people - public or private ]

Sign in to docker hub with your account [say username is : vikashkr117]
Create a repository in docker hub [say : test-docker]
Create a access token and save the password [say access from gitpod IDE ]

When logging in from your Docker CLI client, use this token as a password. Learn more

ACCESS TOKEN DESCRIPTION : gitpod access
ACCESS PERMISSIONS  : Read, Write, Delete
To use the access token from your Docker CLI client:

1. Run docker login -u vikashkr117

2. At the password prompt, enter the personal access token.

Finally to push the image to docker hub

> docker push vikashkr117/test-docker

To remove image "test-inference"

> docker rmi test-inference

docker run --rm -it testimg results


https://timm.fast.ai/


Reduced size by specifying "+cpu" using packages 

torch==1.12.1+cpu

torchvision==0.13.1+cpu


docker ps -a
docker logs <ID> # get ID from above and see console outpu

### References 
1. https://www.cloudbees.com/blog/the-basics-of-the-docker-run-command

2. [Oriellys session](https://github.com/nsadawi/DockerLinReg)- ppt explaination, examples


