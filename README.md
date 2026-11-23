# AKS Azure DevOps Project

Here is a production-style microservices app running on Azure Kubernetes Service (AKS),
provisioned with Terraform and deployed through GitHub Actions.

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
- [ ] Azure resources
- [ ] Kubernetes deployment
- [ ] Ingress, autoscaling, health checks
- [ ] Terraform modules
- [ ] CI/CD pipeline
- [ ] Monitoring and security

## How to Deploy
_Coming soon._

## Cost Notes
_Coming soon._

## What I Learned
_Added as the project grows._
