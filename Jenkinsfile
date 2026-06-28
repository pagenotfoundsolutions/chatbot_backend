pipeline {
    agent any

    environment {
        // Docker Hub - standard URL (no need for parameter)
        DOCKER_REGISTRY = 'docker.io'
        
        // Jenkins Credentials ID for Docker Hub login
        // Configure in: Jenkins → Manage Credentials → Add "Username with password"
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
        
        // Application Name
        APP_NAME = 'chatbot_backend'
    }

    stages {
        // ============================================
        // Stage 1: Set Environment Variables
        // ============================================
        stage('Set Environment') {
            steps {
                script {
                    // Sanitize branch name for Docker tag (replace / with -)
                    env.IMAGE_TAG = env.BRANCH_NAME.replaceAll('/', '-')
                    
                    echo "🚀 Branch: ${env.BRANCH_NAME}"
                    echo "🏷️ Image Tag: ${env.IMAGE_TAG}"
                }
            }
        }

        // ============================================
        // Stage 2: Docker Build & Verify (FastAPI)
        // ============================================
        stage('Docker Build & Verify') {
            steps {
                script {
                    echo "🔨 Building builder image to verify dependencies..."
                    
                    // Build the image to ensure dependencies resolve successfully
                    if (isUnix()) {
                        sh "docker build -f docker/Dockerfile -t ${APP_NAME}:test ."
                    } else {
                        bat "docker build -f docker/Dockerfile -t ${APP_NAME}:test ."
                    }
                    
                    echo "✅ Dependencies verified successfully!"
                }
            }
        }

        // ============================================
        // Stage 3: Docker Build Final Image
        // ============================================
        stage('Docker Build Final Image') {
            when {
                anyOf {
                    branch 'release/*'
                    branch 'hotfix/*'
                }
            }
            steps {
                script {
                    echo "🔨 Building final production image..."
                    
                    // Get Docker Hub username from credentials
                    withCredentials([usernamePassword(
                        credentialsId: DOCKER_CREDENTIALS_ID, 
                        usernameVariable: 'DOCKER_USER', 
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        // Build image name using credentials username
                        def imageName = "${DOCKER_REGISTRY}/${DOCKER_USER}/${APP_NAME}:${env.IMAGE_TAG}"
                        
                        // Docker login (COMMENTED OUT)
                        /*
                        if (isUnix()) {
                            sh "echo ${DOCKER_PASS} | docker login ${DOCKER_REGISTRY} -u ${DOCKER_USER} --password-stdin"
                        } else {
                            bat "echo ${DOCKER_PASS} | docker login ${DOCKER_REGISTRY} -u ${DOCKER_USER} --password-stdin"
                        }
                        */
                        
                        // Build final runtime image
                        def image = docker.build(imageName, "-f docker/Dockerfile .")
                        
                        // Push to Docker Hub (COMMENTED OUT)
                        // image.push()
                        
                        // Logout (COMMENTED OUT)
                        /*
                        if (isUnix()) {
                            sh 'docker logout'
                        } else {
                            bat 'docker logout'
                        }
                        */
                        
                        echo "✅ Docker image built: ${imageName} (push commented out)"
                    }
                }
            }
        }

        // ============================================
        // Stage 4: Deploy to Environment
        // ============================================
        stage('Deploy') {
            when {
                anyOf {
                    // branch 'dev'
                    // branch 'develop'
                     branch 'release'
                    branch 'release/*'
                    branch 'hotfix/*'
                }
            }
            steps {
                script {
                    def composeFile = ''
                    def envFile = ''
                    def envCredentialId = ''
                    def isProd = false
                    
                    // Determine compose file and environment based on branch
                    if (env.BRANCH_NAME == 'dev' || env.BRANCH_NAME == 'develop') {
                        composeFile = 'docker/docker-compose.dev.yml'
                        envFile = 'env/.env.dev'
                        envCredentialId = 'chatbot-env-dev'
                    } else {
                        composeFile = 'docker/docker-compose.prod.yml'
                        envFile = 'env/.env.prod'
                        envCredentialId = 'chatbot-env-prod'
                        isProd = true
                    }
                    
                    echo "📦 Deploying with: ${composeFile} and env file: ${envFile}"
                    
                    // --- OLD CODE (Commented out) ---
                    // // Ensure environment files exist, otherwise use examples
                    // if (isUnix()) {
                    //     sh """
                    //     if [ ! -f "${envFile}" ]; then
                    //         echo "⚠️ ${envFile} not found! Using example file..."
                    //         cp "env/.env.example" "${envFile}"
                    //     fi
                    //     """
                    // } else {
                    //     bat """
                    //     if not exist "${envFile}" (
                    //         echo ⚠️ ${envFile} not found! Using example file...
                    //         copy "env\\.env.example" "${envFile}"
                    //     )
                    //     """
                    // }
                    // --- END OLD CODE ---

                    // Load Environment Variables Securely from Jenkins
                    echo "🔒 Loading environment file for branch '${env.BRANCH_NAME}' using credential ID '${envCredentialId}'..."
                    withCredentials([file(credentialsId: envCredentialId, variable: 'SECRET_ENV')]) {
                        if (isUnix()) {
                            sh "cp \$SECRET_ENV ${envFile}"
                        } else {
                            bat "copy \"%SECRET_ENV%\" \"${envFile}\""
                        }
                    }
                    
                    // Stop existing containers
                    if (isUnix()) {
                        sh "docker compose -f ${composeFile} --env-file ${envFile} down || true"
                    } else {
                        bat "docker compose -f ${composeFile} --env-file ${envFile} down 2>nul || exit 0"
                    }
                    
                    // Start containers
                    if (!isProd) {
                        // Dev: Build locally
                        if (isUnix()) {
                            sh "docker compose -f ${composeFile} --env-file ${envFile} up -d --build"
                        } else {
                            bat "docker compose -f ${composeFile} --env-file ${envFile} up -d --build"
                        }
                    } else {
                        // Prod: Pull image from registry
                        withCredentials([usernamePassword(
                            credentialsId: DOCKER_CREDENTIALS_ID, 
                            usernameVariable: 'DOCKER_USER', 
                            passwordVariable: 'DOCKER_PASS'
                        )]) {
                            def imageName = "${DOCKER_REGISTRY}/${DOCKER_USER}/${APP_NAME}:${env.IMAGE_TAG}"
                            
                            if (isUnix()) {
                                sh "WORKER_IMAGE=${imageName} docker compose -f ${composeFile} --env-file ${envFile} pull app"
                                sh "WORKER_IMAGE=${imageName} docker compose -f ${composeFile} --env-file ${envFile} up -d"
                            } else {
                                bat "set WORKER_IMAGE=${imageName} && docker compose -f ${composeFile} --env-file ${envFile} pull app"
                                bat "set WORKER_IMAGE=${imageName} && docker compose -f ${composeFile} --env-file ${envFile} up -d"
                            }
                        }
                    }
                    
                    // Wait for the containers to be fully up and ready
                    echo "⏳ Waiting for containers to start..."
                    if (isUnix()) {
                        sh "sleep 10"
                    } else {
                        bat "timeout /t 10 /nobreak >nul"
                    }
                    
                    // Run database migrations and seeding
                    echo "🗄️ Running database migrations and seeding..."
                    if (isUnix()) {
                        sh "docker compose -f ${composeFile} --env-file ${envFile} exec -T app alembic upgrade head"
                        sh "docker compose -f ${composeFile} --env-file ${envFile} exec -T app python seeding/seed.py"
                    } else {
                        bat "docker compose -f ${composeFile} --env-file ${envFile} exec -T app alembic upgrade head"
                        bat "docker compose -f ${composeFile} --env-file ${envFile} exec -T app python seeding/seed.py"
                    }
                    
                    echo "✅ Deployed successfully!"
                }
            }
        }
    }

    // ============================================
    // Post Actions
    // ============================================
    post {
        success {
            echo "✅ Pipeline SUCCESS for branch: ${env.BRANCH_NAME}"
        }
        failure {
            echo "❌ Pipeline FAILED for branch: ${env.BRANCH_NAME}"
        }
        always {
            script {
                // Fix permission issues caused by Docker bind mounts running as root
                // This ensures cleanWs() can successfully delete the workspace
                if (isUnix()) {
                    sh 'docker run --rm -v "${WORKSPACE}:/workspace" alpine chown -R $(id -u):$(id -g) /workspace || true'
                }
            }
            cleanWs()
        }
    }
}
