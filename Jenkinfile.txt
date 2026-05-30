pipeline {

    agent any

    stages {

        stage('Verify Repository') {

            steps {

                echo 'Repository cloned successfully'

            }

        }

        stage('Run F5 Automation') {

            steps {

                bat '"C:\\Users\\choud\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" App_Config_LB.py'

            }

        }

    }

    post {

        success {

            echo 'Deployment Successful'

        }

        failure {

            echo 'Deployment Failed'

        }

    }

}