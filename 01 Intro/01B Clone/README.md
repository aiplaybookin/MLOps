

# Docker 

## How to run ?

Clone this repo using `Play with Docker` or `Gitpod`

Build a docker file
```
docker build --tag classify-image .
```

###Who is 🐘 here..
```
docker image history classify-image
```

To run docker (here using default params db.IMAGE & db.MODEL)
```
docker run --rm classify-image
```

To run docker (here custom image link)
```
docker run --rm classify-image db.IMAGE=https://oneworldoneocean.com/wp-content/uploads/2020/07/4975959919_155d6ebb2b_z.jpg
```

To push to Docker hub repository [ to be usd by other teams/ people - public or private ]

Sign in to docker hub with your account [say username is : vikashkr117]
Create a repository in docker hub [say : test-docker]
Create a access token and save the password [say access from gitpod IDE ]

When logging in from your Docker CLI client, use this token as a password.



To remove any dangling builds/images, stopped containers
```
docker system prune
```

