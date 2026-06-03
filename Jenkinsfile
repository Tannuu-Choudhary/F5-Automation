pipeline {

agent any

environment {

    F5_CREDS = credentials('F5_ADMIN')

}

parameters {

    choice(
        name: 'ENVIRONMENT',
        choices: ['DEV', 'QA', 'PROD'],
        description: 'Select Deployment Environment'
    )

    string(
        name: 'APP_NAME',
        defaultValue: 'testapp',
        description: 'Application Name'
    )

    string(
        name: 'VIP_IP',
        defaultValue: '192.169.106.100',
        description: 'Virtual Server IP'
    )

    string(
        name: 'VIP_PORT',
        defaultValue: '80',
        description: 'Virtual Server Port'
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

            echo "Selected Environment: ${params.ENVIRONMENT}"

            echo "Application Name: ${params.APP_NAME}"

        }

    }

    stage('Environment Validation') {

        steps {

            script {

                if (params.ENVIRONMENT == 'DEV') {

                    echo 'DEV Environment Selected'

                }
                else if (params.ENVIRONMENT == 'QA') {

                    echo 'QA Environment Selected'

                }
                else {

                    echo 'PROD Environment Selected'

                }

            }

        }

    }

    stage('Set Environment Variables') {

        steps {

            script {

                if (params.ENVIRONMENT == 'DEV') {

                    env.TARGET_F5 = '192.168.35.129'

                }
                else if (params.ENVIRONMENT == 'QA') {

                    env.TARGET_F5 = '192.168.35.129'

                }
                else {

                    env.TARGET_F5 = '192.168.35.129'

                }

                echo "Target F5 = ${env.TARGET_F5}"

            }

        }

    }

    stage('Production Approval') {

        when {

            expression {
                params.ENVIRONMENT == 'PROD'
            }

        }

        steps {

            input(
                message: 'Approve Production Deployment?',
                ok: 'Deploy'
            )

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
