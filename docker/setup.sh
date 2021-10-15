#!/bin/bash
# You need to change followings:
DIR_DOCKER_FILE="./docker"
DOCKER_IMAGE_NAME="whata/ge_s1_downloader:latest"
DOCKER_CONTAINER_NAME="whata_ge_s1"
MEMORY="24G"

echo "*******************************"
echo "Start creating docker image"
docker build --network host -t $DOCKER_IMAGE_NAME $DIR_DOCKER_FILE --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)
echo "Finished creating docker image"
echo "*******************************"

echo "Start creating docker container"
docker run --net host \
           -v $(pwd):/workspace \
           --shm-size=$MEMORY \
           --name $DOCKER_CONTAINER_NAME \
           -itd $DOCKER_IMAGE_NAME
echo "Finished creating docker container"
echo "*******************************"