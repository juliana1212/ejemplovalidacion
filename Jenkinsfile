pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY = 'CRUD-Clientes-DevOps'
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
                pytest --cov=src --cov-report=xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                    . $VENV_DIR/bin/activate

                    curl -sSLo sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
                    unzip -o sonar-scanner.zip
                    export PATH=$PATH:$(pwd)/sonar-scanner-5.0.1.3006-linux/bin

                    sonar-scanner \
                      -Dsonar.projectKey=$SONAR_PROJECT_KEY \
                      -Dsonar.projectName="$SONAR_PROJECT_NAME" \
                      -Dsonar.sources=src \
                      -Dsonar.python.coverage.reportPaths=coverage.xml
                    '''
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
    }

    post {
        always {
            archiveArtifacts artifacts: 'coverage.xml', fingerprint: true
        }
    }
}
