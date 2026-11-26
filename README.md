# AKS Azure DevOps Project

A production-style microservices app running on Azure Kubernetes Service (AKS),
provisioned with Terraform and deployed through GitHub Actions.
Built step by step as a hands-on cloud and DevOps portfolio project.

## Architecture
_Diagram coming in a later step._

## The Application
A small visit counter made of three containers:
- **frontend**: NGINX serving a web page, forwarding `/api/` requests to the API
- **api**: Python (Flask + Gunicorn); counts visits and reports which container served the request
- **redis**: stores the counter

### Run locally
```bash
cd app
docker compose up --build
```
Then open http://localhost:8080

## Tech Stack
Azure (AKS, ACR), Kubernetes, Docker, Terraform, GitHub Actions, Prometheus, Grafana

## Project Status
- [x] Repo structure
- [x] App and containers
- [x] Container registry (ACR) and images
- [ ] AKS cluster
- [ ] Kubernetes deployment
- [ ] Ingress, autoscaling, health checks
- [ ] Terraform modules
- [ ] CI/CD pipeline
- [ ] Monitoring and security

## Azure Setup (manual)
First pass: resources created by hand with the Azure CLI to learn what each piece does.
A later step replaces this with Terraform.

Prerequisites: Azure CLI, kubectl, Docker Desktop, and `az login`.

```bash
RG=rg-aks-project
LOCATION=northeurope
ACR_NAME=<globally-unique-name>
AKS_NAME=aks-project-dev

# Resource group and container registry
az group create --name $RG --location $LOCATION
az acr create --resource-group $RG --name $ACR_NAME --sku Basic

# Build for amd64 and push to the registry
az acr login --name $ACR_NAME
docker buildx build --platform linux/amd64 -t $ACR_NAME.azurecr.io/api:v1 --push ./app/api
docker buildx build --platform linux/amd64 -t $ACR_NAME.azurecr.io/frontend:v1 --push ./app/frontend
```

Cluster (in progress; the VM size must be one your subscription allows and has quota for):

```bash
az aks create --resource-group $RG --name $AKS_NAME --node-count 1 \
  --node-vm-size <allowed-vm-size> --tier free --generate-ssh-keys --attach-acr $ACR_NAME
az aks get-credentials --resource-group $RG --name $AKS_NAME
```

## Cost Notes
- The AKS control plane is on the free tier; the worker node VMs are billed for every hour they run.
- Pause the cluster when not in use: `az aks stop --resource-group $RG --name $AKS_NAME`
  (resume with `az aks start`).
- Delete everything when finished: `az group delete --name $RG --yes`

## How to Deploy
_Coming soon._

## What I Learned
Real problems hit while building this, and how I solved them:
- **Region not accepting new customers:** West Europe refused new resources for my subscription.
  Switched to North Europe.
- **ACR Tasks blocked:** `az acr build` is not permitted on every subscription, so images are
  built locally with `docker buildx` and pushed to the registry.
- **Apple-chip laptops build arm64 images, AKS nodes need amd64:** fixed by building with
  `--platform linux/amd64`.
- **VM size not allowed or no quota:** a VM size has to pass two checks, being available to the
  subscription in that region and having vCPU quota for its family. Checked allowed sizes and
  `az vm list-usage` to pick one that passes both.
