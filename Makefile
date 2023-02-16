## Get environment variables
PORT := 3000

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

## Local Development operations

# Install required dependencies
dependencies-install:
	pip3 install -r requirements.txt

# Run application
run-dev:
	python3 src/api.py

# Run application
run:
	waitress-serve --port $(PORT) api:app	

## Docker operations

# Build and tag Docker image
build-image:
	docker image build . --build-arg port=$(PORT) -t sfiorini/python-k8s-sample:v1.0.0  -t sfiorini/python-k8s-sample:latest

# Publish Docker image
publish-image:
	docker push sfiorini/python-k8s-sample --all-tags

# Create and run Container from Docker image
create-run-container:
	docker run -d --name python-k8s-sample -p $(PORT):$(PORT) sfiorini/python-k8s-sample:latest

# Start Container
start:
	docker container start python-k8s-sample

# Stop Container
stop:
	docker container stop python-k8s-sample

# Remove Container
remove-container:
	docker container rm python-k8s-sample

# Remove Image
remove-image:
	docker images -a | grep "sfiorini/python-k8s-sample" | awk '{print $$3}' | xargs docker rmi -f

# Stop Container, Remove Container and Remove Image
docker-uninstall:
	make stop;make remove-container;make remove-image

# Create Docker Image, Container and Start Container
docker-install:
	make build-image && make create-run-container

## Kubernetes

# Install NGINX Ingress Controller 
install-ingress-controller:
	kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.5.1/deploy/static/provider/cloud/deploy.yaml

# Deploy application's pod
deploy-k8s-deployment:
	./utils/vars_replacer.sh -i ./kube/python-k8s-sample.yaml -p "PORT=$(PORT)" | kubectl apply -f -

# Deploy application's service
deploy-k8s-service:
	./utils/vars_replacer.sh -i ./kube/python-k8s-sample-service.yaml -p "PORT=$(PORT)" | kubectl apply -f -

# Deploy application's ingress
deploy-k8s-ingress:
	./utils/vars_replacer.sh -i ./kube/python-k8s-sample-ingress.yaml -p "PORT=$(PORT)" | kubectl apply -f -

# Remove application's pod
delete-k8s-deployment:
	kubectl delete deployments python-k8s-sample-deployment

# Remove application's service
delete-k8s-service:
	kubectl delete service python-k8s-sample-service

# Remove application's ingress
delete-k8s-ingress:
	kubectl delete ingress python-k8s-sample-ingress

# Full install of application on cluster
k8s-install:
	make deploy-k8s-deployment && make deploy-k8s-service && make deploy-k8s-ingress

# Full uninstall of application from cluster
k8s-uninstall:
	make delete-k8s-ingress && make delete-k8s-service && make delete-k8s-deployment