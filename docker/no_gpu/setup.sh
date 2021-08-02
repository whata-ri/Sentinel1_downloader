# You need to change followings:
DIR_DOCKER_FILE="./docker/no_gpu"
DOCKER_IMAGE_NAME="satellite_v1"
DOCKER_CONTAINER_NAME="satellite"
MEMORY="8G"

cd $DIR_DOCKER_FILE
echo "*******************************"
echo "Start creating docker image"
docker build --network host -t $DOCKER_IMAGE_NAME .
echo "Finished creating docker image"
echo "*******************************"

echo "Start creating docker container"
docker run --net host \
           -v /home/ec2-user/workspace/Sentinel1_downloader:/workspace \
           --shm-size=$MEMORY \
           --name $DOCKER_CONTAINER_NAME \
           -itd $DOCKER_IMAGE_NAME
echo "Finished creating docker container"