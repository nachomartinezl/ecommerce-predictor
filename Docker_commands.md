# Automated product categorization for e-commerce with AI

- Docker build:

```bash
$ docker build -t finalproject -f docker/Dockerfile .
```

- Docker run:

```bash
$ docker run --rm --net host -it \
    -v $(pwd):/home/app/src \
    finalproject \
    bash
```