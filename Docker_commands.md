# Automated product categorization for e-commerce with AI

- Docker build:

```bash
$ docker build -t finalproject -f docker/Dockerfile .
$ docker build -t finalproject --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -f docker/Dockerfile .
```

- Docker run:

```bash
$ docker run --rm --net host -it \
    -v $(pwd):/home/app/src \
    finalproject \
    bash
```