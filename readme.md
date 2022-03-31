# Docker and Kubernetes intro

This repository is about the second assignment of the cloud computing course.

> Instructor: [Dr. S. A. Javadi](https://scholar.google.com/citations?user=Va7RTUsAAAAJ&hl=en)

> Semester: Winter 2022

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
## Section 3: Kubernetes
First, we create a ConfigMap called `server-config.yaml` with the following format:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: server-config
data:
  weather_url: "http://api.weatherstack.com/current?access_key=b3324a714ee5cdb9ec8d2bf1d83b824c&query=Tehran"
  server_port: "8000"
```
As we can see, there are two data that are the values from the ENV variables set on our server. To apply the config on our cluster ConfigMaps, we enter the following command:
```text
kubectl apply -f server-config.yaml
```
We can get the list of config maps using the following command:
```text
kubectl get configmaps
```

Following the creation of the config map, we need to create a deployment to run our pods. So we create it using the following command:
```text
kubectl create deployment <deployment-name> --image=<image-name> --dry-run=client -o yaml > server-deployment.yaml
```
In the preceding command, ``--dry-run=client`` flag means that we want to get a preview of the object instead of creating
it in our cluster. Additionally, `-o yaml` means that our output format is `yaml` and we store the content on the
`server-deployment.yaml` file.

After the modification of the created file, we have the following content:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: server-deployment
  name: server-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: server-deployment
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: server-deployment
    spec:
      containers:
      - image: soroushmehraban2022/weather-server:1.0
        name: weather-server
        env:
          - name: server_port
            valueFrom:
              configMapKeyRef:
                name: server-config
                key: server_port
          - name: weather_url
            valueFrom:
              configMapKeyRef:
                name: server-config
                key: weather_url
        resources: {}
status: {}
```
There are two modifications that are made:
- **replicas: 2**: this means to create 2 pods.
- **env**: this sets the env variables of our container. We have to environment variables that we get the values from 
  the created config map. 
  
Next, we apply the created deployment:
```text
kubectl apply -f server-deployment.yaml
```

We can get the status of our pods on our deployment using the following command:
```text
kubectl get deployments
```
After a while, we should see the following content:
```text
NAME                READY   UP-TO-DATE   AVAILABLE   AGE
server-deployment   2/2     2            2           <START TIME HERE>
```
Note that the both pods are ready. So we can get their IP address by entering this command:
```text
> kubectl get pods -o wide
NAME                                 READY   STATUS             RESTARTS   AGE     IP           NODE       NOMINATED NODE   READINESS GATES
server-deployment-5b8d668949-gf8wv   1/1     Running            0          <TIME>   172.17.0.3   minikube   <none>           <none>
server-deployment-5b8d668949-rnktd   1/1     Running            0          <TIME>   172.17.0.4   minikube   <none>           <none>
```
As we can see, there are two pods with different names. They both start with `server-deployment` which is the deployment
that manages them. followed by `5b8d668949` which is the deployment tag and then another tag which is unique for each pod.

One of the drawbacks of using pods directly is that their IP Address might change after each restart. Hence, we create a
server to automatically manages these two pods and distribute the incoming traffic over them.

To create the service, first we create the following content on `server-service.yaml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: server-service
spec:
  selector:
    app: server-deployment
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
```
- The `selector app` refers to the deployment that is going to manage its pods.
- `targetPort: 8000` is the container ports that we assigned on the config map.
- `port: 80` is the port of the service.

After the creation of the service, we apply it using the following command:
```text
kubectl apply -f server-service.yaml
```
Getting the services:
```text
> kubectl get services
NAME             TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
kubernetes       ClusterIP   10.96.0.1      <none>        443/TCP   14h
server-service   ClusterIP   10.97.53.201   <none>        80/TCP    <TIME>
```

The relation between the service and the pods:
```text
> kubectl get ep
NAME             ENDPOINTS                         AGE
kubernetes       192.168.49.2:8443                 14h
server-service   172.17.0.3:8000,172.17.0.4:8000   <TIME>
```
As we can see from the `ep` (endpoints), the server-service is connected to the IP addresses of our deployment's pods.
## Section 4: Testing the system
Now we want to test the created service. So we create a pod from the image created on section 1 and send an HTTP get request to the service using `curl`.

First, we try creating a new pod called `curl-pod` using the following command:
```text
> kubectl run curl-pod --image=soroushmehraban2022/new-alpine:1.0
pod/curl-pod created

> kubectl get pods
NAME                                 READY   STATUS             RESTARTS      AGE
curl-pod                             0/1     CrashLoopBackOff   1 (6s ago)    8s
server-deployment-5b8d668949-gf8wv   1/1     Running            1 (23m ago)   <TIME>
server-deployment-5b8d668949-rnktd   1/1     Running            1 (23m ago)   <TIME>
```
As we see from the result of the second command, the status of the created pod is `CrashLoopBackOff`. According to the
[sysdig](https://sysdig.com/blog/debug-kubernetes-crashloopbackoff/), "A CrashloopBackOff means that you have a pod starting, crashing, starting again, and then crashing again." 

As a solution, we can define a deployment to create this pod and execute the `sleep` command in an infinite amount. Like the previous section, we enter the following command:

```text
kubectl create deployment curl-deployment --image=soroushmehraban2022/new-alpine:1.0 --dry-run=client -o yaml > curl-deployment.yaml
```
Then we modify the container part as follows:
```yaml
    spec:
      containers:
      - image: soroushmehraban2022/new-alpine:1.0
        name: new-alpine
        command: ["/bin/sleep"]
        args: ["infinite"]
        resources: {}
```
Finally, we apply the deployment using the following command:
```text
kubectl apply -f curl-deployment.yaml
```

By entering the following command, we can see the pod is up and running:
```text
> kubectl get deployments
NAME                READY   UP-TO-DATE   AVAILABLE   AGE
curl-deployment     1/1     1            1           37s
server-deployment   2/2     2            2           <TIME>

> kubectl get pods
NAME                                 READY   STATUS    RESTARTS      AGE
curl-deployment-6f95cf5f47-lrt6c     1/1     Running   0             43s
server-deployment-5b8d668949-gf8wv   1/1     Running   1 (11m ago)   <TIME>
server-deployment-5b8d668949-rnktd   1/1     Running   1 (11m ago)   <TIME>
```

Last but not least, we can execute the pod's ash and send HTTP requests to the `server-service`:
```text
> kubectl exec curl-deployment-6f95cf5f47-lrt6c -it -- ash
/ # curl server-service
{"hostname":"server-deployment-5b8d668949-rnktd","temperature":20,"weather_descriptions":["Partly cloudy"],"wind_speed":11,"humidity":12,"feelslike":20}/ #
/ # curl server-service
{"hostname":"server-deployment-5b8d668949-rnktd","temperature":20,"weather_descriptions":["Partly cloudy"],"wind_speed":11,"humidity":12,"feelslike":20}/ #
/ # curl server-service
{"hostname":"server-deployment-5b8d668949-rnktd","temperature":20,"weather_descriptions":["Partly cloudy"],"wind_speed":11,"humidity":12,"feelslike":20}/ #
/ # curl server-service
{"hostname":"server-deployment-5b8d668949-rnktd","temperature":20,"weather_descriptions":["Partly cloudy"],"wind_speed":11,"humidity":12,"feelslike":20}/ #
/ # curl server-service
{"hostname":"server-deployment-5b8d668949-gf8wv","temperature":20,"weather_descriptions":["Partly cloudy"],"wind_speed":11,"humidity":12,"feelslike":20}/ #
/ # curl server-service
{"hostname":"server-deployment-5b8d668949-gf8wv","temperature":20,"weather_descriptions":["Partly cloudy"],"wind_speed":11,"humidity":12,"feelslike":20}/ #
/ # curl server-service
{"hostname":"server-deployment-5b8d668949-rnktd","temperature":20,"weather_descriptions":["Partly cloudy"],"wind_speed":11,"humidity":12,"feelslike":20}/ #
/ # curl server-service
{"hostname":"server-deployment-5b8d668949-gf8wv","temperature":20,"weather_descriptions":["Partly cloudy"],"wind_speed":11,"humidity":12,"feelslike":20}/ #
/ # 
```
As we can see, the service automatically distributes the request between the pods as the name of the hostname is different between different requests.
