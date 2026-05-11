pipeline {
    agent any
    environment {
        APP_IMAGE  = "xemon99/ocr-api"
        EXCEPTION_MSG = ""
    }
    stages {
        /* checkout the Jenkinsfile */
        stage('Checkout') {
            steps {
                echo"===> Checkout scm <==="
                checkout scm
            }
        }
        /* check tag if it has or not */
        stage('Validate Tag') {
            steps {
                echo "===> Validate Tag <==="
                script {
                    try {
                        env.VERSION = getValidTag()
                        echo "✅ Release tag detected: ${env.VERSION}"
                    } catch (Exception error) {
                        env.EXCEPTION_MSG = error.toString()
                        throw error
                    }

                }
            }
        }
        /* build to artifact and push to docker hub */
        stage('Build & Push Docker Images') {
            steps {
                echo "===> Build image and push server <==="
                script {
                     try {
                        dockerBuildAndPush(APP_IMAGE,env.VERSION)
                        echo "✅ push successfully : )"
                     }catch(Exception error) {
                        env.EXCEPTION_MSG = error.toString()
                        throw error
                     }
                }
            }
        }
    }
}

// ** validation tag repo **
def getValidTag() {
    def tag = env.TAG_NAME.trim()
    if (!tag) {
        error("❌ No tag found on this commit. Docker build requires a release tag.")
    }
//     ex: prod-v0.0.2 or dev-v0.0.2 or uat-v0.0.2 , ex: if tag 'v0.2.1' it mean release new version
    if ( tag ==~ /^prod-v?\d+\.\d+\.\d+$/ || tag ==~ /^uat-v?\d+\.\d+\.\d+$/ || tag ==~ /^dev-v?\d+\.\d+\.\d+$/ || tag ==~ /^v?\d+\.\d+\.\d+$/) {
        return tag
    }else {
        error("❌ Invalid tag format: ${tag}")
    }
}
// ** docker login and push to docker hub **
def dockerBuildAndPush(imageName, version) {
    withCredentials([
        usernamePassword(
            credentialsId: 'docker-hub',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASS'
        )
    ]) {
        if(env.VERSION ==~ /^dev-v.*/ || env.VERSION ==~ /^prod-v.*/ || env.VERSION ==~ /^uat-v.*/){
            sh """
                  set -e
                  echo "🐳 Building ${imageName}:${version}"
                  echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                  docker build -t ${imageName}:${version} .
                  docker tag ${imageName}:${version} ${imageName}:lts
                  docker push ${imageName}:${version}
                  docker push ${imageName}:lts
            """
        }else if (env.VERSION ==~ /^v.*/){
            sh """
                  set -e
                  echo "🐳 Building ${imageName}:${version}"
                  echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                  docker build -t ${imageName}:${version} .
                  docker push ${imageName}:${version}
               """
        }
    }
}