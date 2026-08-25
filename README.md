# Jenkins CI/CD Pipeline with Docker, GitOps, Argo CD and Kubernetes

This project demonstrates a CI/CD workflow for a containerized Python Flask application using Jenkins, Docker, GitHub, Argo CD, and Kubernetes.

Jenkins handles continuous integration tasks such as dependency installation, automated testing, Docker image creation, and image publishing. Deployment configuration is maintained separately in a GitOps repository. Jenkins updates the container image tag in that repository, and Argo CD synchronizes the change with Kubernetes.

## Architecture

```text
Developer
   ↓
GitHub Application Repository
   ↓
Jenkins
   ↓
Install Dependencies
   ↓
Run Automated Tests
   ↓
Build Docker Image
   ↓
Push Docker Image to Registry
   ↓
Update GitOps Repository
   ↓
Argo CD Detects Git Change
   ↓
Kubernetes
   ↓
Cloud App Deployment
```

## Application Repository Structure

```text
jenkins-ci-pipeline/
├── app/
│   ├── __init__.py
│   ├── app.py
│   └── requirements.txt
├── tests/
│   └── test_app.py
├── .gitignore
├── Dockerfile
├── Jenkinsfile
└── README.md
```

## Technologies Used

- Jenkins
- Docker
- Python
- Flask
- Gunicorn
- Pytest
- Git
- GitHub
- Kubernetes
- Argo CD
- GitOps

## Application

The project contains a small Flask application used to demonstrate the CI/CD workflow.

The application provides:

- `/` — application status endpoint
- `/health` — health-check endpoint used by Kubernetes readiness and liveness probes

The application runs on port `5000`.

## Automated Testing

Pytest is used to verify the application before a container image is built.

The tests check that:

- The main endpoint responds successfully.
- The application reports a `running` status.
- The health endpoint responds successfully.
- The application reports a `healthy` status.

This allows Jenkins to stop the pipeline if application tests fail.

## Docker

The application is packaged as a Docker container.

The Dockerfile:

1. Uses a Python 3.12 slim base image.
2. Installs the application dependencies.
3. Copies the Flask application into the image.
4. Exposes port `5000`.
5. Runs the application with Gunicorn.

## Jenkins Pipeline

The `Jenkinsfile` defines the CI workflow.

The pipeline performs the following stages:

1. Checkout source code.
2. Install Python dependencies.
3. Run automated tests.
4. Build the Docker image.
5. Push the image to the container registry.
6. Update the image tag in the GitOps repository.

Credentials are referenced through Jenkins credentials rather than stored directly in the repository.

## GitOps Deployment

Kubernetes deployment configuration is maintained in a separate repository:

`alexcgodwin/cloud-app-gitops`

The Jenkins pipeline updates the container image reference in that repository after a successful build.

Argo CD monitors the GitOps repository and synchronizes the desired configuration with the Kubernetes cluster.

This separates the CI process from Kubernetes deployment and keeps Git as the source of truth for the desired application state.

## Kubernetes

The GitOps repository contains:

- Namespace configuration
- Deployment configuration
- Kubernetes Service
- Argo CD Application configuration

The application Deployment uses two replicas and a rolling update strategy.

Kubernetes readiness and liveness probes use the application's `/health` endpoint.

## Argo CD

Argo CD monitors the `kubernetes` directory of the GitOps repository.

Automated synchronization is configured with:

- Automatic sync
- Pruning
- Self-healing

When Jenkins changes the Docker image tag in Git, Argo CD detects the new desired state and applies it to Kubernetes.

## Security Practices

This project follows several basic security practices:

- Credentials are not hard-coded in the Jenkinsfile.
- Jenkins credentials are used for external authentication.
- Environment files are excluded through `.gitignore`.
- Secrets are not committed to the repositories.
- Application and deployment configuration are maintained separately.

## CI/CD Workflow

```text
Code Change
    ↓
GitHub
    ↓
Jenkins Pipeline
    ↓
Automated Tests
    ↓
Docker Build
    ↓
Container Registry
    ↓
GitOps Repository Update
    ↓
Argo CD
    ↓
Kubernetes Deployment
```

## Project Goal

The goal of this project is to demonstrate a practical CI/CD and GitOps workflow where Jenkins handles continuous integration and image creation, while Argo CD handles Kubernetes continuous delivery from a Git-controlled desired state.
