pipeline {

    agent any

    environment {

        F5_CREDS = credentials('F5_ADMIN')

    }

    parameters {

        string(
            name: 'APP_NAME',
            defaultValue: 'testapp'
        )

        string(
            name: 'VIP_IP',
            defaultValue: '192.169.106.100'
        )

        string(
            name: 'VIP_PORT',
            defaultValue: '80'
        )

        string(
            name: 'POOL_MEMBERS',
            defaultValue: '192.168.35.130,192.168.35.131'
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

}