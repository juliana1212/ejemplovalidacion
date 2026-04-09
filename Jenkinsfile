pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY = 'crud-clientes-devops'
        SONAR_PROJECT_NAME = 'CRUD Clientes DevOps'
        VENV_DIR = '.venv'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv $VENV_DIR
                . $VENV_DIR/bin/activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests with Coverage') {
            steps {
                sh '''
                . $VENV_DIR/bin/activate
                python -m pytest
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                    . .venv/bin/activate
                    pip install sonar-scanner-cli
                    sonar-scanner \
                      -Dsonar.projectKey=crud-clientes-devops \
                      -Dsonar.sources=src \
                      -Dsonar.python.coverage.reportPaths=coverage.xml
                    '''
                }
            }
        }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t crud-clientes-api .
                '''
            }
        }

        stage('Deploy API') {
            steps {
                sh '''
                docker rm -f crud-clientes-api-container || true
                docker run -d --name crud-clientes-api-container -p 8000:8000 crud-clientes-api
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'coverage.xml', fingerprint: true
        }
    }
}
