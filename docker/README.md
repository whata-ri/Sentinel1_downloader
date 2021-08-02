## 1. Docker settings
```shell
sudo systemctl start docker
cd docker/<gpu> or <no_gpu>
sudo docker build --network host -t $DOCKER_IMAGE_NAME .
```