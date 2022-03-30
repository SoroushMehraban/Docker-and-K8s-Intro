# Docker and Kubernetes intro
This repository is about the second assignment of the cloud computing course.

## Section 1: Docker Hub
This section creates a `Dockerfile` that has an alpine linux distribution with curl installed.

To make an image from this Dockerfile, we have to go to the `1. DockerHub` directory and build the image using the following command:
```text
docker build -t <image-name>:<tag> .
```
In the preceding command, we specified to build the Dockerfile existing in the current directory (which is the `.`), and
name it `<image-name>` with the `<tag>` tag.


Next, before pushing to the Docker Hub, we change the tag with the following command:
```text
docker tag <image-name>:<tag> <docker-id>/<image-name>:<tag>
```
In the preceding command, we create a tag named `<docker-id>/<image-name>:<tag>` that refers to `<image-name>:<tag>`. 
`<docker-id>` is the docker ID of the Docker Hub account. by doing this, when we want to push the image it automatically detects which repository to push.

For pushing into Docker Hub, we can enter the following command:
``
docker image push <docker-id>/<image-name>:<tag>
``
