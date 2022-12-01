## AWS Lambda
[No Servers, Just Code]


Initially people used to have zip files with all requirements, code, model, weights etc. however we will be using ```Docker images deploy```.


### Firecracker
AWS created FireCracker, a virtualization service for Lambda. 

Firecracker enables you to deploy workloads in lightweight virtual machines, called ```microVMs```, which provide ```enhanced security and workload isolation``` over traditional VMs, while enabling the ```speed and resource efficiency``` of containers. Firecracker was developed at Amazon Web Services to improve the customer experience of services like ```AWS Lambda``` and ```AWS Fargate```.

Read more [here](https://firecracker-microvm.github.io)

### Serverless Framework

AWS is tech partner however cloud agnostic. https://www.serverless.com/

***How or Why?*** 

Instead of manually creating Lambda function, API Gateway, making connections and S3 bucket creation we will be using serverless framework to deploy via code. We just need to provide the docker.


### AWS Lambda

What is ```Handler```,```Event``` and ```Context``` ?

Read [here](https://aws-lambda-for-python-developers.readthedocs.io/en/latest/02_event_and_context/#event)
- Can elaborate here what event and context contains


Use AWS EC2 instance - minimum ```t3a.medium``` . Check prices [here](https://aws.amazon.com/ec2/pricing/on-demand/)

1. Install node js
```
curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -

sudo apt install nodejs
```

2. Install serverless ```sudo npm i -g serverless```

Test 
```
serverless --help
which serverless
```

3. Configuration to be done in ```serverless.yml``` file. Create this file.

- memorySize : set it to max i.e. 10gb and later see usage and reduce accordingly. Lambda has around 10gb of memory.
- timeout : check you use case, ideally we will be able to do in within 5 mins, so 300 seconds.
- image : docker image placed in ECR

Create a Docker image -> Push to ECR -> deploy using serverless

```
service: serverless-mnist
 
provider:
  name: aws #cloud provider
  region: ap-southeast-2 #region (sydney)
  memorySize: 10240 #memory usage
  timeout: 300 
 
functions:
  mnist:
    image: 006547668672.dkr.ecr.ap-southeast-2.amazonaws.com/mnist-serverless:latest 
    events:
      - http:
          path: inference 
          method: post 
          cors: true
```

Docker image :

NOTE : We will have to use ```AWS Lambda base image```

If you use some other base image then use ```AWS Lambda Python Runtime Interface Client``` to make it work for lambda in AWS.

LAMBDA_TASK_ROOT : Env variable defined in base image. This has read/write access. So we are using for pip installs.

Set command : Pointing to that specific function. Lambda will call this function.

docker images


Run and Test 

```docker run --rm -it -p 8080:8080 cifar-serverless```

```
curl --location --request POST 'http://localhost:8080/2015-03-31/functions/function/invocations' \
--header 'Content-Type: application/json' \
--data-raw '{
    "body": "data:image/png;base64,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"
}'
```

Output received -
<Placeimagehere>

Run duration, Memory usage, Event what was received, .....lambda test func arn-not yet deployed
<Placeimagehere>


Now we can deploy to AWS -

First we need to ```push docker image to ECR```. We will be using private repo.

- Got to ECR, Create a private repo - just give name. Next copy commands for the build and push and execute 

NOTE : You need to have AWS CLI installed.

Once uploaded to ECR. Copy the image URI and paste in ```serverless.yml``` image. Check region and other stuffs.


IAM Permissions to enable to work -

````AWSCloudFormationFullAccess
AmazonAPIGatewayAdministrator
CloudWatchLogsFullAccess
AWSLambda_FullAccess
AmazonS3FullAccess````


Deploy ```serverless deploy```

<Placeimagehere>
endpoint url will be shown on console

Go to cloud formation -> stacks -> check steps, resources, click lambda and see. 

Test the deployed endpoint URL using https://hoppscotch.io or postman.

By default stage is set to ```dev``` 

Link to Lamda : https://199uo09gd1.execute-api.ap-southeast-2.amazonaws.com/dev/inference

```
Deploying serverless-cifar to stage dev (ap-southeast-2)
Warning: Serverless Dashboard doesn't support functions that reference AWS ECR images
Warning: Function cifar has timeout of 300 seconds, however, it's attached to API Gateway so it's automatically limited to 30 seconds.

✔ Service deployed to stack serverless-cifar-dev (153s)

dashboard: https://app.serverless.com/aiplaybookin/apps/serverless-cifar/serverless-cifar/dev/ap-southeast-2
endpoint: POST - https://199uo09gd1.execute-api.ap-southeast-2.amazonaws.com/dev/inference
functions:
  cifar: serverless-cifar-dev-cifar
```

To remove 

```serverless remove```




## -----

Difference between ```wsgi``` and ```asgi```

Flask uses wsgi and Fastapi uses asgi

## --------- Frontend -----

Next js build on top of react js

1. clone repo https://github.com/satyajitghana/emlov2-serverless

2. cd to folder, install yarn ```sudo npm i -g yarn```

3. Run ```yarn``` . This will install all packages mentioned in ```package.json``` similar to requirements.txt

4. make sure node js is of version 16.x

```node --version```

5. Install next js https://beta.nextjs.org/docs/installation

6. Run ```yarn dev```

Open the port mentioned in output url in the security group of ec2.

Take public ip of ec2 : 3.25.181.89:3000


## Others 

- ```Glances``` alternative to ```htop``` .
pip install glances

- If permission denied post docker installations
```sudo chmod 777 /var/run/docker.sock```

- Read about AWS Lambda, [here](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html)

- Disc space check ```df -h``` 

- FRONTEND : tailwindcss, next js, react js

ssh-keygen -t rsa -b 4096 -C "aiplaybook.in@gmail.com"

Your identification has been saved in /home/ubuntu/.ssh/id_rsa
Your public key has been saved in /home/ubuntu/.ssh/id_rsa.pub

