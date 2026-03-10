pipeline {
    agent any

    environment {
        VENV = "venv"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('CI - Setup Environment') {
            steps {
                sh '''
                python3 -m venv $VENV
                source $VENV/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('CI - Validate Scripts') {
            steps {
                sh '''
                source $VENV/bin/activate
                python -m py_compile api_collector.py
                python -m py_compile monitor.py
                '''
            }
        }

        stage('CD - Execute Monitoring') {
            when {
                changeRequest()
            }

            steps {
                sh '''
                source $VENV/bin/activate
                python api_collector.py
                python monitor.py
                '''
            }
        }

    }
}
