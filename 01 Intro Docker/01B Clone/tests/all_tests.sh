#!/bin/bash

source ./tests/utils.sh

echo "🧪 Start tests"

CONTAINER_NAME=emlov2:session-01

## Test build container

RUN_OUT=$(docker build -t $CONTAINER_NAME .)

if [ $? -eq 0 ]; then
	echo "✅ Build container success"
else
	echo "❌ Docker build failed !"
	exit 1
fi

## Test run container

for MODEL in resnet18 vit_base_patch16_224 coat_tiny
do
	RUN_OUT=$(docker run $CONTAINER_NAME db.MODEL=$MODEL db.IMAGE=https://github.com/pytorch/hub/raw/master/images/dog.jpg)

	if [ $? -eq 0 ]; then
		echo "✅ Run $MODEL success"
	else
		echo "❌ Run failed for $MODEL !, got: $RUN_OUT"
		exit 1
	fi

	## Test if output is valid json

	python3 -c "import json; json.loads('$RUN_OUT')"

	if [ $? -eq 0 ]; then
		echo "✅ Output is valid json"
	else
		echo "❌ Output is not valid json ! got: $RUN_OUT"
		exit 1
	fi
done

## Test to check pytorch version in image

PYTORCH_VERSION=$(docker run --entrypoint "" $CONTAINER_NAME python3 -c "import torch; print(torch.__version__.split('+')[0])")

if V $PYTORCH_VERSION '>=' 1.10; then
	echo "✅ Pytorch version is $PYTORCH_VERSION > 1.10"
else
	echo "❌ Pytorch version is $PYTORCH_VERSION < 1.10"
	exit 1
fi

echo "✅ All tests passed"

exit 0