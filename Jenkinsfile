pipeline {
    agent { node { label 'master' } }
    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '100'))
    }
    triggers {
        cron('0 0 * * *')
    }
    stages {
        stage('Run cleanup script') {
            steps {
                withCredentials([usernamePassword(
                        credentialsId: 'CLEANUP_BOT_FOR_ARTIFACTORY',
                        usernameVariable: 'ARTIFACTORY_USERNAME',
                        passwordVariable: 'ARTIFACTORY_PASSWORD')]) {
                    sh 'python cleanup.py'
                }
            }
        }
    }
}
