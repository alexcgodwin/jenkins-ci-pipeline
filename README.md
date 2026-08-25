# Cloud Application CI/CD Pipeline with Jenkins, Docker, Argo CD and Kubernetes

A practical DevOps project demonstrating an automated CI/CD and GitOps workflow using Jenkins, Docker, GitHub, Argo CD and Kubernetes.

The pipeline tests a Python application, builds a Docker image, publishes the image to Docker Hub, updates a separate GitOps repository, and allows Argo CD to automatically synchronize the new application version with Kubernetes.

## Architecture

```text
Developer
    |
    v
GitHub Application Repository
    |
    v
Jenkins
    |
    +---- Checkout Source Code
    |
    +---- Install Python Dependencies
    |
    +---- Run Automated Tests
    |
    +---- Build Docker Image
    |
    +---- Push Image to Docker Hub
    |
    v
Update GitOps Repository
    |
    v
GitHub GitOps Repository
    |
    v
Argo CD
    |
    v
Kubernetes Cluster
    |
    v
Cloud Application
```

## Technologies Used

- Jenkins
- GitHub
- Git
- Python
- Pytest
- Docker
- Docker Hub
- Kubernetes
- Argo CD
- GitOps
- YAML

## CI/CD Workflow

### 1. Source Code Checkout

Jenkins retrieves the application source code and Jenkinsfile from GitHub.

### 2. Dependency Installation

The pipeline creates an isolated Python virtual environment and installs the application's dependencies.

### 3. Automated Testing

Pytest runs the automated tests before a container image is created.

A failed test stops the pipeline and prevents the application from progressing to the image publishing and deployment stages.

### 4. Docker Image Build

After the tests pass, Jenkins builds the application container image.

Each successful pipeline run uses the Jenkins build number as the Docker image tag.

Example:

```text
alexcgodwin/cloud-app:5
```

This provides a clear link between a Jenkins build and the corresponding container image.

### 5. Docker Hub Push

Jenkins authenticates to Docker Hub using credentials stored securely in Jenkins Credentials and publishes the newly built image.

Credentials are not stored directly inside the Jenkinsfile.

### 6. GitOps Repository Update

After publishing the image, Jenkins clones the deployment repository:

```text
cloud-app-gitops
```

The pipeline updates the Kubernetes deployment manifest with the new Docker image tag, commits the change, and pushes it to GitHub.

### 7. Argo CD Synchronization

Argo CD monitors the GitOps repository.

When Jenkins changes the Kubernetes manifest, Argo CD detects the difference between the desired state stored in Git and the current state of the Kubernetes cluster.

Automatic synchronization applies the new desired state to the cluster.

The application is configured with:

```text
Auto-Sync: Enabled
Prune: Enabled
Self Heal: Enabled
```

### 8. Kubernetes Deployment

The application runs in the Kubernetes namespace:

```text
devops-demo
```

The deployment currently runs two application replicas behind a Kubernetes ClusterIP service.

Verification:

```bash
kubectl get all -n devops-demo
```

A successful deployment shows two running application pods and two available deployment replicas.

## Application Verification

For local testing, the Kubernetes service can be forwarded to the workstation:

```bash
kubectl port-forward service/cloud-app 8082:80 -n devops-demo
```

The application can then be accessed at:

```text
http://localhost:8082
```

Successful response:

```json
{
  "application": "cloud-app",
  "message": "CI/CD pipeline deployment successful",
  "status": "running"
}
```

## GitOps Design

This project separates continuous integration from Kubernetes deployment.

Jenkins is responsible for:

- Checking out source code
- Installing dependencies
- Running automated tests
- Building the Docker image
- Publishing the image
- Updating the GitOps repository

Argo CD is responsible for:

- Monitoring the Kubernetes configuration stored in Git
- Detecting configuration changes
- Synchronizing the desired state with Kubernetes
- Detecting deployment drift
- Maintaining the configured GitOps state

This separation means Jenkins does not need to directly execute the Kubernetes deployment.

Git remains the source of truth for the desired Kubernetes configuration.

## Repository Structure

Example project structure:

```text
jenkins-ci-pipeline/
│
├── app/
│   ├── requirements.txt
│   └── ...
│
├── tests/
│   └── ...
│
├── Dockerfile
├── Jenkinsfile
└── README.md
```

The Kubernetes manifests are maintained separately in:

```text
cloud-app-gitops
└── kubernetes/
    └── deployment.yaml
```

## Jenkins Credentials

The pipeline uses Jenkins Credentials rather than placing authentication secrets in source control.

Configured credentials include:

```text
dockerhub-credentials
github-gitops-credentials
```

The Docker Hub credential allows Jenkins to publish container images.

The GitHub credential allows Jenkins to update the GitOps repository.

## Successful Result

The completed workflow demonstrates:

```text
Code Change
    ↓
Jenkins CI
    ↓
Automated Tests
    ↓
Docker Image Build
    ↓
Docker Hub
    ↓
GitOps Manifest Update
    ↓
Argo CD
    ↓
Kubernetes
    ↓
Running Application
```

The final environment was verified with:

- Successful Jenkins pipeline execution
- Docker image publication
- Successful GitOps repository update
- Argo CD showing `Healthy`
- Argo CD showing `Synced`
- Argo CD reporting `Sync OK`
- Two Kubernetes application replicas running
- Zero application pod restarts during verification
- Successful application response through the Kubernetes service

## Key DevOps Concepts Demonstrated

This project demonstrates practical experience with:

- Continuous Integration
- Continuous Delivery
- GitOps
- Pipeline as Code
- Automated testing
- Containerization
- Container image versioning
- Kubernetes deployments
- Declarative infrastructure configuration
- Automated synchronization
- Deployment drift detection
- Credential management
- Separation of CI and CD responsibilities

## Future Improvements

Possible production-focused improvements include:

- Replace local Kubernetes with a managed Kubernetes platform such as Amazon EKS
- Add container vulnerability scanning
- Add static code analysis
- Add Kubernetes health checks and resource requests/limits where appropriate
- Add Prometheus and Grafana monitoring
- Add centralized application logging
- Add TLS and ingress
- Add environment-specific GitOps configurations
- Add controlled promotion between development, staging and production
- Add image signing and stronger software supply-chain controls
