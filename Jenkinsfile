pipeline {
    agent any
    environment {
        PATH = "/opt/homebrew/bin:/usr/local/bin:${env.PATH}"
        DOCKERHUB_USER = 'YOUR_DOCKERHUB_USER'
        IMAGE = "${DOCKERHUB_USER}/cloud-image:${BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build and Test') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                python -m py_compile app.py
                '''
            }
        }
        stage('Docker Build') {
            steps { sh 'docker build -t ${IMAGE} .' }
        }
        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials',
                                 usernameVariable: 'U', passwordVariable: 'P')]) {
                    sh 'echo "$P" | docker login -u "$U" --password-stdin'
                    sh 'docker push ${IMAGE}'
                }
            }
        }
        stage('Deploy to Minikube') {
            steps {
                sh '''
                sed "s|IMAGE_PLACEHOLDER|${IMAGE}|" k8s/deployment.yaml | kubectl apply -f -
                kubectl apply -f k8s/service.yaml
                kubectl rollout status deployment/flask-app --timeout=180s
                '''
            }
        }
        stage('Verify') {
            steps {
                sh '''
                kubectl get pods,deployment,svc
                kubectl port-forward svc/flask-service 5050:5000 >/dev/null 2>&1 &
                PF=$!
                sleep 5
                curl -s http://localhost:5050
                kill $PF
                '''
            }
        }
    }
    post {
        success { echo 'Pipeline completed successfully!' }
        failure { echo 'Pipeline failed!' }
    }
}
