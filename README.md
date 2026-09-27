# ResilienceOps

**ResilienceOps** is an end-to-end DevOps project focused on **Kubernetes resilience, self-healing, containerization, and CI/CD automation on AWS**.

The project demonstrates how a containerized application can be automatically tested, built, pushed to Amazon ECR, and deployed to Amazon EKS using GitHub Actions and AWS OIDC authentication.

The project also demonstrates Kubernetes self-healing by running multiple replicas and automatically recreating a Pod when one is deleted or fails.

---

## 🏗️ Architecture

```text
                         GitHub
                            │
                            │ Push
                            ▼
                  GitHub Actions CI/CD
                            │
                  ┌─────────┴─────────┐
                  │                   │
                Pytest              AWS OIDC
                  │                   │
                  │                   ▼
                  │              IAM Role
                  │                   │
                  │                   ▼
                  │                  ECR
                  │                   │
                  │            Docker Image
                  │                   │
                  └──────────► EKS Deployment
                                      │
                                      ▼
                              Kubernetes Service
                                      │
                                      ▼
                              AWS Load Balancer
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                   ResilienceOps Pod         ResilienceOps Pod
                         │                         │
                         └────────────┬────────────┘
                                      │
                                    FastAPI
                                      │
                                  PostgreSQL
```

---

## 🚀 Features

* FastAPI REST API
* Swagger / OpenAPI documentation
* PostgreSQL database
* SQLAlchemy ORM
* Docker containerization
* Docker Compose for local development
* Automated tests with Pytest
* GitHub Actions CI/CD
* AWS IAM OIDC authentication
* Amazon ECR container registry
* Amazon EKS Kubernetes cluster
* Kubernetes Deployment with 2 replicas
* Kubernetes readiness and liveness probes
* Kubernetes LoadBalancer Service
* Kubernetes self-healing
* Infrastructure as Code with Terraform
* AWS networking and IAM configuration

---

## 🛠️ Technology Stack

| Technology      | Purpose                       |
| --------------- | ----------------------------- |
| Python          | Application                   |
| FastAPI         | REST API                      |
| PostgreSQL      | Database                      |
| SQLAlchemy      | ORM                           |
| Pytest          | Testing                       |
| Docker          | Containerization              |
| Docker Compose  | Local environment             |
| GitHub Actions  | CI/CD                         |
| AWS IAM         | Identity and permissions      |
| AWS OIDC        | GitHub → AWS authentication   |
| Amazon ECR      | Container registry            |
| Amazon EKS      | Kubernetes                    |
| Kubernetes      | Container orchestration       |
| Terraform       | Infrastructure as Code        |
| Swagger/OpenAPI | API testing and documentation |

---

## 📁 Project Structure

```text
ResilienceOps/
├── app/
│   ├── __init__.py
│   ├── database.py
│   └── main.py
│
├── tests/
│   └── test_health.py
│
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
│
├── terraform/
│   ├── ecr.tf
│   ├── eks.tf
│   ├── github_oidc.tf
│   ├── iam.tf
│   ├── networking.tf
│   ├── outputs.tf
│   └── provider.tf
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── create_tables.py
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# 💻 Local Development

## 1. Clone the repository

```bash
git clone git@github.com:yahiaouiraouf216/Resilienceops.git
cd ResilienceOps
```

## 2. Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Start PostgreSQL

```bash
docker compose up -d
```

## 5. Run the application

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

---

# 🧪 Testing

Run the test suite:

```bash
pytest
```

The project currently includes automated health-check testing.

Example:

```text
2 passed
```

Tests are automatically executed by GitHub Actions before deployment.

---

# 🐳 Docker

Build the image locally:

```bash
docker build -t resilienceops .
```

Run the container:

```bash
docker run -p 8000:8000 resilienceops
```

Test:

```text
http://localhost:8000/health
```

---

# ☁️ AWS Infrastructure

Terraform provisions the AWS infrastructure required by ResilienceOps.

The infrastructure includes:

* VPC
* Public subnets
* Internet Gateway
* Security groups
* IAM roles
* ECR repository
* EKS cluster
* EKS managed node group
* GitHub Actions OIDC provider
* GitHub Actions IAM role

AWS region:

```text
ca-central-1
```

Initialize Terraform:

```bash
cd terraform
terraform init
```

Review the infrastructure:

```bash
terraform plan
```

Apply:

```bash
terraform apply
```

---

# 🔐 GitHub Actions → AWS Authentication

The CI/CD pipeline uses **AWS OIDC** instead of storing long-lived AWS access keys inside GitHub Secrets.

The authentication flow is:

```text
GitHub Actions
      │
      │ OIDC Token
      ▼
GitHub OIDC Provider
      │
      ▼
AWS IAM Role
      │
      ▼
Temporary AWS Credentials
```

This allows GitHub Actions to authenticate to AWS using temporary credentials.

No permanent:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

are required for the deployment workflow.

---

# 🔄 CI/CD Pipeline

Every Pull Request runs the test stage.

A push to `main` triggers the deployment pipeline.

```text
Git Push
   │
   ▼
Checkout
   │
   ▼
Install Python dependencies
   │
   ▼
Run Pytest
   │
   ├── FAIL → Stop
   │
   ▼
Configure AWS using OIDC
   │
   ▼
Authenticate with ECR
   │
   ▼
Build Docker image
   │
   ▼
Push image to ECR
   │
   ▼
Configure kubectl
   │
   ▼
Connect to EKS
   │
   ▼
Deploy Kubernetes manifests
   │
   ▼
Wait for rollout
   │
   ▼
Verify Pods and Service
```

Docker images are tagged using the Git commit SHA.

Example:

```text
resilienceops:<commit-sha>
```

This provides traceability between a deployment and the exact source-code version that produced it.

---

# ☸️ Kubernetes

The application runs as a Kubernetes Deployment with **2 replicas**.

Example:

```yaml
replicas: 2
```

Each Pod exposes:

```text
Port: 8000
```

The application uses:

### Readiness Probe

```text
/health
```

The readiness probe tells Kubernetes whether the application is ready to receive traffic.

### Liveness Probe

```text
/health
```

The liveness probe allows Kubernetes to detect an unhealthy container and restart it when necessary.

---

# 🌐 Application Access

The Kubernetes Service uses:

```text
type: LoadBalancer
```

AWS provisions an external Load Balancer that exposes the application to the Internet.

Swagger:

```text
/docs
```

Health endpoint:

```text
/health
```

---

# 🛡️ Self-Healing Demonstration

One of the main objectives of ResilienceOps is demonstrating Kubernetes self-healing.

The Deployment maintains two replicas.

Check the Pods:

```bash
kubectl get pods -o wide
```

Example:

```text
NAME                             READY   STATUS
resilienceops-xxxxx-xxxxx        1/1     Running
resilienceops-yyyyy-yyyyy        1/1     Running
```

Delete one Pod intentionally:

```bash
kubectl delete pod <pod-name>
```

Watch Kubernetes:

```bash
kubectl get pods -w
```

Kubernetes detects that the desired number of replicas is no longer available and automatically creates a replacement Pod.

Expected behavior:

```text
Pod deleted
    ↓
Replica count = 1
    ↓
Deployment detects missing replica
    ↓
New Pod created
    ↓
Container starts
    ↓
Readiness probe succeeds
    ↓
Replica count = 2
```

This demonstrates a fundamental Kubernetes self-healing mechanism.

---

# 📊 Resilience Testing

Future resilience scenarios planned for the project include:

* Pod deletion
* Container failure
* Application health failure
* Increased latency
* Service failure
* Resource exhaustion
* Automated recovery
* Monitoring and alerting
* Incident tracking
* Mean Time To Recovery (MTTR)

---

# 🎯 Project Objectives

This project was built to demonstrate practical DevOps skills rather than only theoretical knowledge.

The main objectives are:

1. Build a containerized application.
2. Test the application automatically.
3. Build and publish Docker images.
4. Implement secure GitHub → AWS authentication.
5. Provision AWS infrastructure using Terraform.
6. Deploy an application to Kubernetes.
7. Implement health checks.
8. Demonstrate Kubernetes self-healing.
9. Build a foundation for chaos engineering and observability.

---

# 📚 DevOps Skills Demonstrated

### Linux

* Command-line administration
* SSH
* Processes
* Networking
* File permissions
* Troubleshooting

### Git

* Branches
* Commits
* Pull Requests
* GitHub workflows

### Docker

* Dockerfiles
* Images
* Containers
* Docker Compose
* Container networking

### AWS

* IAM
* VPC
* ECR
* EKS
* EC2
* Security Groups
* OIDC

### Terraform

* Infrastructure as Code
* AWS provider
* Resources
* Variables
* Outputs
* Terraform state
* Dependency management

### Kubernetes

* Pods
* Deployments
* Services
* Replicas
* Health probes
* LoadBalancer
* Self-healing
* kubectl

### CI/CD

* GitHub Actions
* Automated testing
* Docker image builds
* ECR deployment
* Kubernetes deployment
* Deployment verification

---

# 🔮 Future Improvements

The next evolution of ResilienceOps will focus on production-style resilience and observability:

```text
                    ResilienceOps
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       CI/CD Pipeline          Kubernetes
                                     │
                           ┌─────────┴─────────┐
                           ▼                   ▼
                      Monitoring          Chaos Tests
                           │                   │
                           ▼                   ▼
                      Prometheus           Failures
                           │                   │
                           ▼                   ▼
                       Grafana          Self-Healing
                           │
                           ▼
                    Incident Metrics
                           │
                           ▼
                          MTTR
```

Planned additions:

* Prometheus
* Grafana
* Alertmanager
* Kubernetes HPA
* Chaos experiments
* Incident timeline
* Automated remediation
* MTTR dashboard
* Production-style monitoring

---

# 👨‍💻 Author

**Yahia Ouiraouf**

DevOps / Cloud Engineer — Montréal, Canada

GitHub:

`github.com/yahiaouiraouf216`

---

## ⭐ Project Status

**Current status: CI/CD + AWS + Kubernetes deployment completed.**

The application is successfully:

```text
Tested
  ↓
Containerized
  ↓
Pushed to ECR
  ↓
Deployed to EKS
  ↓
Exposed through AWS Load Balancer
  ↓
Running with 2 Kubernetes replicas
  ↓
Self-healing demonstrated
```

The next phase is **observability + chaos engineering**.
