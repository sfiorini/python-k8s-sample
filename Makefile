## Docker operations

# Build Docker image
build-image:
	docker image build . -t sfiorini/python-k8s-sample:v1.0.0  -t sfiorini/python-k8s-sample:latest

# Publish Docker image
publish-image:
	docker push sfiorini/python-k8s-sample --all-tags

# Run Docker image
create-run-container:
	docker run -d --name python-k8s-sample -p 3000:3000 sfiorini/python-k8s-sample:latest

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

docker-uninstall:
	make stop;make remove-container;make remove-image

docker-install:
	make build-image && make create-run-container

## Kubernetes

install-ingress-controller:
	kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.5.1/deploy/static/provider/cloud/deploy.yaml

deploy-k8s-deployment:
	kubectl apply -f ./kube/python-k8s-sample.yaml

deploy-k8s-service:
	kubectl apply -f ./kube/python-k8s-sample-service.yaml

deploy-k8s-ingress:
	kubectl apply -f ./kube/python-k8s-sample-ingress.yaml

delete-k8s-deployment:
	kubectl delete deployments python-k8s-sample-deployment

delete-k8s-service:
	kubectl delete service python-k8s-sample-service

delete-k8s-ingress:
	kubectl delete ingress python-k8s-sample-ingress

k8s-install:
	make deploy-k8s-deployment && make deploy-k8s-service && make deploy-k8s-ingress

k8s-uninstall:
	make delete-k8s-ingress && make delete-k8s-service && make delete-k8s-deployment