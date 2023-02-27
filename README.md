# Python K8s Sample

## Description

This repository contains a sample template for deploying a 
[Python](https://www.python.org/) application to [Kubernetes](https://kubernetes.io/).

## Usage

### Installing

For the purpose of running the sample, we are basing this document on deploying on a local [Kubernetes](https://kubernetes.io/) installation that is provided by [Docker Desktop](https://www.docker.com/products/docker-desktop/).

The project provides a `makefile` with all the commands needed to install and deploy the application.

---
#### Dependencies
You will need to make sure that the following dependencies are installed on your system:
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/)and make sure you enable [Kubernetes](https://kubernetes.io/)
  - [Python](https://www.python.org/) version 3.9 and above.
  - [GNU Make](https://www.gnu.org/software/make/)
  - [Lens](https://k8slens.dev/) (Optional: for UI view and control of K8s clusters)

---
#### Setup Development Environment
 - Clone this repository
 - Copy `.env.sample` to `.env` and set the evironment variables as indicated in the help within the file.
 - Install dependencies:
    ```bash
    make dependencies-install
    ```
    or
    
    ```bash
    pip3 install -r requirements.txt
    ```
 - Run application
    ```bash
    make run-dev
    ```
     or
    
    ```bash
    python3 src/api.py
    ```
 - Open browser at http://localhost:3000 and you should get the following response.
   ```json
   {
    "message": "API Server is running successfully"
   }
   ```
---
#### Run in a Docker container
 - Create [Docker](https://www.docker.com) image (Note: the following command adds 2 tags, as latest and the current version of the app):
    ```bash
    docker image build . -t sfiorini/python-k8s-sample:v1.0.0  -t sfiorini/python-k8s-sample:latest
    ```
     or
    
    ```bash
    make build-image
    ```
  - Create and run [Docker](https://www.docker.com) container:
    ```bash
    docker run -d --name python-k8s-sample -p 3000:3000 sfiorini/python-k8s-sample:latest
    ```
     or
    
    ```bash
    make create-run-container
    ```
  - Open browser at http://localhost:3000 and you should get the following response.
    ```json
    {
      "message": "API Server is running successfully"
    }
    ```
  
  Fore all other [Docker](https://www.docker.com) commands, please see the [Makefile](#makefile-section) reference below.

---
#### Run in Kubernetes

- Create [Docker](https://www.docker.com) image: See above section.
- Publish [Docker](https://www.docker.com) image to registry.  
  For this tutorial we assume publishing on [Docker Hub](https://hub.docker.com/), however the same script will work with all other compatible registries.  
  Registry account setup is beyond the scope of this documentation.
  ```bash
  docker push sfiorini/python-k8s-sample --all-tags
  ```
     or
    
  ```bash
  make publish-image
  ```
- Install [NGINX Ingress Controller](https://docs.nginx.com/nginx-ingress-controller/) on [Kubernetes](https://kubernetes.io/) cluster for [Docker Desktop](https://www.docker.com/products/docker-desktop/).  
  Note: This is a one time operation as part of setup for the cluster. For commmercial installation, more than likely the `Ingress Controller` is already installed by your administrator.
  ```bash
  kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.5.1/deploy/static/provider/cloud/deploy.yaml
  ```
     or
    
  ```bash
  make install-ingress-controller
  ```
- Deploy application's pod.  
  Open `./kube/python-k8s-sample.yaml` and replace `${PORT}` with the port declared on your `.env` file (Default: 3000).

  ```bash
  kubectl apply -f ./kube/python-k8s-sample.yaml
  ```
     or
    
  ```bash
  make deploy-k8s-deployment
  ```
- Deploy application's service.   
  Open `./kube/python-k8s-sample-service.yaml` and replace `${PORT}` with the port declared on your `.env` file (Default: 3000).

  ```bash
  kubectl apply -f ./kube/python-k8s-sample-service.yaml
  ```
     or
    
  ```bash
  make deploy-k8s-service
  ```  
- Deploy application's ingress.   
  Open `./kube/python-k8s-sample-ingress.yaml` and replace `${PORT}` with the port declared on your `.env` file (Default: 3000).
  ```bash
  kubectl apply -f ./kube/python-k8s-sample-ingress.yaml
  ```
     or
    
  ```bash
  make deploy-k8s-ingress
  ```
 - Open browser at http://your-k8s-domain:3000 and you should get the following response.  
 NOTE: [Docker Desktop](https://www.docker.com/products/docker-desktop/) adds domain `kubernetes.docker.internal` to the hosts file. Therefore your url will be http://kubernetes.docker.internal:3000.

    ```json
    {
      "message": "API Server is running successfully"
    }
    ```
Fore all other [kubectl](https://kubernetes.io/docs/reference/kubectl/) commands, please see the [Makefile](#makefile-section) reference below.

---        
### Folder structure

Here's the project's folder structure:

```
/python-k8s-sample  # Root directory.
|- .vscode/         # Folder containing config files to develop the app using VSCode.
|- kube/            # Kubernetes deployment yaml files.
|- .gitignore       # Ignore patterns for git.
|- src              # The location of source files for the Python application
|- Dockerfile       # Metadata content (title, author...).
|- Makefile         # Makefile used for building our documents.
|- README.md        # Documentation (this file)
|- requirements.txt # Application's dependencies
```
---
### <a name="makefile-section"></a>Makefile commands
See below a complete list of `make` commands for installation and maintenance of the application:

| Command                   | Section       |  Description | 
| -----                     | ----          | ----
| dependencies-install      | Development   | Install required dependencies
| run                       | Development   | Run application service
| bump-version-patch        | Development   | Bumps version's patch
| bump-version-minor        | Development   | Bumps version's minor
| bump-version-major        | Development   | Bumps version's major
| build-image               | Docker        | Build and tag Docker image
| publish-image             | Docker        | Publish Docker image to registry
| create-run-container      | Docker        | Create and run Container from Docker image
| start                     | Docker        | Start Docker Container
| stop                      | Docker        | Stop Docker Container
| remove-container          | Docker        | Remove Docker Container
| remove-image              | Docker        | Remove Docker Image
| docker-install            | Docker        | Create Docker Image, Container and Start Container
| docker-uninstall          | Docker        | Stop Container, Remove Container and Remove Image
| install-ingress-controller| Kubernetes    | Install NGINX Ingress Controller 
| deploy-k8s-deployment     | Kubernetes    | Deploy application's pod
| deploy-k8s-service        | Kubernetes    | Deploy application's service
| deploy-k8s-ingress        | Kubernetes    | Deploy application's ingress
| delete-k8s-deployment     | Kubernetes    | Remove application's pod
| delete-k8s-service        | Kubernetes    | Remove application's service
| delete-k8s-ingress        | Kubernetes    | Remove application's ingress
| k8s-install               | Kubernetes    | Full install of application on cluster
| k8s-uninstall             | Kubernetes    | Full uninstall of application from cluster 

---
## References

- [Python](https://www.python.org/)
- [Kubernetes](https://kubernetes.io/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GNU Make](https://www.gnu.org/software/make/)
- [Lens](https://k8slens.dev/)
- [Docker Hub](https://hub.docker.com/)
- [NGINX Ingress Controller](https://docs.nginx.com/nginx-ingress-controller/)
- [kubectl](https://kubernetes.io/docs/reference/kubectl/)
