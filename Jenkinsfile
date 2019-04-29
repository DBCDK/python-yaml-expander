pipeline {
    agent { label "stretch" }
    triggers {
        pollSCM("H/3 * * * *")
    }
    options {
        buildDiscarder(logRotator(artifactDaysToKeepStr: "", artifactNumToKeepStr: "", daysToKeepStr: "30", numToKeepStr: "30"))
        timestamps()
    }
    environment {
        RSYNC_TARGET = credentials('debian-rsync-stretch')
    }
    stages {
        stage("build") {
            steps {
                script {
                    if (! env.BRANCH_NAME) {
                        currentBuild.rawBuild.result = Result.ABORTED
                        throw new hudson.AbortException('Job Started from non MultiBranch Build')
                    } else {
                        println(" Building BRANCH_NAME == ${BRANCH_NAME}")
                    }
                }
                script {
                    sh "./build.sh"
                }
            }
        }
        stage("upload") {
            steps {
                script {
                    if (env.BRANCH_NAME ==~ /master/) {
                        sh '''
                        	cd deb_dist && for changes in *.changes; do rsync -av $changes `sed -e '1,/^Files:/d' -e '/^[A-Z]/,$d' -e 's/.* //' $changes` ${RSYNC_TARGET}; done
                        '''
                    }
                }
            }
        }
    }
}
