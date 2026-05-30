pipeline {

    agent any

    parameters {

        string(
            name: 'APP_NAME',
            defaultValue: 'testapp',
            description: 'Application Name'
        )

        string(
            name: 'VIP_IP',
            defaultValue: '192.169.106.100',
            description: 'VIP Address'
        )

        string(
            name: 'VIP_PORT',
            defaultValue: '80',
            description: 'VIP Port'
        )

        string(
            name: 'POOL_MEMBERS',
            defaultValue: '192.168.35.130,192.168.35.131',
            description: 'Comma Separated Pool Members'
        )

    }

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