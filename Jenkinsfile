pipeline {
    agent any
    environment {
        AWS_REGION     = 'ap-south-1'
        AWS_ACCOUNT_ID = '729147111409'
        ECR_REPOSITORY = 'image-regi'
        IMAGE_NAME     = 'cloud-image'
        ECR_REGISTRY   = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        ECR_IMAGE = "${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build and Test') {
            steps {
                sh 'python3 -m pip install --user -r requirements.txt'
                sh 'python3 -m py_compile app.py'
            }
        }
        stage('Docker Build') {
            steps { sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .' }
        }
        stage('ECR Login') {
            steps {
                sh '''
                aws ecr get-login-password --region ${AWS_REGION} |
                docker login --username AWS --password-stdin ${ECR_REGISTRY}
                '''
            }
        }
        stage('Docker Tag') {
            steps { sh 'docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${ECR_IMAGE}' }
        }
        stage('Push to ECR') {
            steps { sh 'docker push ${ECR_IMAGE}' }
        }
        stage('Deploy to Kubernetes') {
    steps {
        sh '''
        kubectl create secret docker-registry ecr-secret \
          --docker-server=${ECR_REGISTRY} \
          --docker-username=AWS \
          --docker-password="$(aws ecr get-login-password --region ${AWS_REGION})" \
          --dry-run=client -o yaml | kubectl apply -f -

        sed "s|IMAGE_PLACEHOLDER|${ECR_IMAGE}|" k8s/deployment.yaml | kubectl apply -f -
        kubectl apply -f k8s/service.yaml
        kubectl rollout status deployment/flask-app --timeout=120s
        '''
    }
}
    }
    post {
        success { echo 'Pipeline completed successfully!' }
        failure { echo 'Pipeline failed!' }
    }
}
