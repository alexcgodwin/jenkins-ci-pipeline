pipeline {

    agent any

    environment {
        DOCKER_IMAGE = "alexcgodwin/cloud-app"
        DEPLOYMENT_FILE = "kubernetes/deployment.yaml"
        VENV = ".venv"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv "$VENV"
                    . "$VENV/bin/activate"

                    python -m pip install --upgrade pip
                    python -m pip install -r app/requirements.txt
                    python -m pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . "$VENV/bin/activate"
                    pytest -v tests/
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh """
                    docker build \
                    -t ${DOCKER_IMAGE}:${BUILD_NUMBER} .
                """
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" |
                        docker login \
                        -u "$DOCKER_USER" \
                        --password-stdin
                    '''

                    sh """
                        docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}
                    """
                }
            }
        }

        stage('Update GitOps Repository') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-gitops-credentials',
                        usernameVariable: 'GIT_USERNAME',
                        passwordVariable: 'GIT_TOKEN'
                    )
                ]) {
                    sh '''
                        set -e

                        rm -rf gitops-repo

                        git clone \
                        "https://${GIT_USERNAME}:${GIT_TOKEN}@github.com/alexcgodwin/cloud-app-gitops.git" \
                        gitops-repo

                        cd gitops-repo

                        git config user.name "Jenkins CI"
                        git config user.email "alex.godwin@alexemekagodwin.com"

                        sed -i \
                        "s|image: .*cloud-app:.*|image: ${DOCKER_IMAGE}:${BUILD_NUMBER}|g" \
                        "${DEPLOYMENT_FILE}"

                        git add "${DEPLOYMENT_FILE}"

                        if git diff --cached --quiet; then
                            echo "No GitOps changes detected."
                        else
                            git commit \
                                -m "Deploy cloud-app image ${BUILD_NUMBER}"

                            git push origin main
                        fi
                    '''
                }
            }
        }
    }

    post {

        success {
            echo '''
            CI pipeline completed successfully.
            Container image published.
            GitOps repository updated.
            '''
        }

        failure {
            echo '''
            CI pipeline failed.
            Review the Jenkins build logs.
            '''
        }

        always {
            sh '''
                docker logout || true
                rm -rf gitops-repo || true
            '''
        }
    }
}
