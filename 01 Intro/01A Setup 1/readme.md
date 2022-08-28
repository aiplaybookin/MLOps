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