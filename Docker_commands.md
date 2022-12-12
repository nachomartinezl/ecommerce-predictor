# Automated product categorization for e-commerce with AI

- Docker build:

```bash
$ docker build -t finalproject -f docker/Dockerfile .
$ docker build -t finalproject --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -f docker/Dockerfile2 .
$ docker build -t finalproject_gpu --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -f docker/Dockerfile_gpu .
```

- Docker run:

```bash
$ docker run --rm --net host -it \
    -v $(pwd):/home/app/src \
    finalproject \
    bash

$ docker run --rm --net host --gpus all -it \
    -v $(pwd):/home/app/src \
    --workdir /home/app/src \
    finalproject_gpu \
    bash
```