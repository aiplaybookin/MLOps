# syntax = docker/dockerfile:1.2
FROM python:3.10
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu:/usr/local/nvidia/lib64:/usr/local/nvidia/bin
COPY .cog/tmp/build923784970/cog-0.0.1.dev-py3-none-any.whl /tmp/cog-0.0.1.dev-py3-none-any.whl
RUN --mount=type=cache,target=/root/.cache/pip pip install /tmp/cog-0.0.1.dev-py3-none-any.whl
RUN --mount=type=cache,target=/root/.cache/pip pip install   torch==1.12.1 torchvision==0.13.1 timm==0.6.7
WORKDIR /src
EXPOSE 5081
CMD ["python", "-m", "cog.server.http"]
COPY . /src
