# Docker and Kubernetes intro

This repository is about the second assignment of the cloud computing course.

## Section 1: Docker Hub

This section creates a `Dockerfile` that has an alpine linux distribution with curl installed.

To make an image from this Dockerfile, we have to go to the `1. DockerHub` directory and build the image using the
following command:

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
`<docker-id>` is the docker ID of the Docker Hub account. by doing this, when we want to push the image it automatically
detects which repository to push.

Finally, for pushing into Docker Hub, we can enter the following command:  
``
docker image push <docker-id>/<image-name>:<tag>
``

## Section 2: Weather Server

In this section, a simple HTTP REST server is implemented using FastAPI. it only has one endpoint that takes a GET
request and returns the following response:

```json
{
  "hostname": "<SERVER HOSTNAME>",
  "temperature": "<CURRENT TEMPERATURE>",
  "weather_descriptions": "<WEATHER DESCRIPTIONS>",
  "wind_speed": "<WIND SPEED>",
  "humidity": "<HUMIDITY>",
  "feelslike": "<FEELS LIKE>"
}
```
To get the temperature info, it sends an HTTP GET to a server that its URL is set on `weather_url` environment variables. 
Additionally, `server_port` env variable is also set so that the server port is configurable.

A `Dockerfile` is also included on `2. WeatherServer` directory. In this step, we create an image and push to the Docker Hub using the commands mentioned in the previous section.

Last but not least, we can test the created image locally using the following command:
```text
docker run --rm --env weather_url="http://api.weatherstack.com/current?access_key=<ACCESS_KEY>&query=Tehran" -p 80:8080 <docker-id>/<image-name>:<tag>
```
In the preceding command:
- **--rm**: removes the container after the execution.
- **--env**: Sets the required environment variables which are `weather_url` and `server_port`. Since `server_port` is not set, the python code sets to the default value which is 8080.
- **-p**: Maps port with the structure `<HOST-PORT>:<CONTAINER-PORT>`. Therefore, it maps the port 8080 of the container to the 80 of the host.


