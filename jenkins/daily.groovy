def dirname = "library_reservation"

pipeline{
    agent{
        label "master"
    }
    parameters {
        booleanParam(name: "SHORT_CLASSIFY", defaultValue: false,
                     description: "If true, shorten book number for classifying"
        )
    }
    stages{
        stage("Git Checkout for Docker Build"){
            steps{
                dir("/home/ec2-user/library_reservation") {
                    echo "======== Executing Git Checkout for Docker Build ========"
                    sh 'git checkout .'
                    sh 'git pull'
                }
            }
        }
        stage("Docker Build"){
            steps{
                echo "======== Executing Docker Build ========"
                dir("/home/ec2-user/library_reservation/docker") {
                    sh 'source ./docker_build.sh'
                }
            }
        }
        stage("Git Checkout for Docker Container"){
            agent {
                docker {
                  image 'library_reservation:latest'
                  args "-e TZ=Asia/Tokyo" // the number of args statement should not be over one
                }
            }
            steps{
                script {
                    if(fileExists("${dirname}")){
                        sh "rm -rf ${dirname}"
                    }
                }
                sh "git clone https://github.com/sarcastic555/library_reservation.git"
                sh "mkdir -p ${dirname}/list"
            }
        }
        stage("Download Booklist"){
            agent {
                docker {
                  image 'library_reservation:latest'
                  args '-e TZ=Asia/Tokyo'
                }
            }
            steps{
                dir("./${dirname}"){
                    echo "======== Executing Download Booklist ========"
                    sh "python ./download_booklist.py"
                }
            }
        }
        stage("Extension Checker"){
            agent {
                docker {
                  image 'library_reservation:latest'
                  args '-e TZ=Asia/Tokyo'
                }
            }
            steps{
                dir("./${dirname}"){
                    echo "======== Executing Extension Checker ========"
                    sh "python extension_checker.py"
                }
            }
        }
        stage("Create Owning or Reserving Booklist"){
            agent {
                docker {
                  image 'library_reservation:latest'
                  args '-e TZ=Asia/Tokyo'
                }
            }
            steps{
                dir("./${dirname}"){
                    echo "======== Executing Create Owning or Reserving Booklist ========"
                    sh "python ./create_owning_or_reserving_booklist.py"
                }
            }
        }
        stage("Classify Booklist"){
            agent {
                docker {
                  image 'library_reservation:latest'
                  args '-e TZ=Asia/Tokyo'
                }
            }
            steps{
                script {
                    command = "python ./classify_list.py"
                    if (params.SHORT_CLASSIFY){
                        command += " --short"
                    }
                    dir("./${dirname}"){
                        echo "======== Executing Classify Booklist ========"
                        sh "${command}"
                    }
                }
            }
        }
        stage("Send Line Message"){
            agent {
                docker {
                  image 'library_reservation:latest'
                  args '-e TZ=Asia/Tokyo'
                }
            }
            steps{
                dir("./${dirname}"){
                    echo "======== Executing Send Line Message ========"
                    sh "python ./send_line_message.py"
                }
            }
        }
        stage("Clear Reservation Basket"){
            agent {
                docker {
                  image 'library_reservation:latest'
                  args '-e TZ=Asia/Tokyo'
                }
            }
            steps{
                dir("./${dirname}"){
                    echo "======== Executing Clear Reservation Basket ========"
                    sh "python ./clear_reserve_basket.py"
                }
            }
        }
        stage("Reserve Book"){
            agent {
                docker {
                  image 'library_reservation:latest'
                  args '-e TZ=Asia/Tokyo'
                }
            }
            steps{
                dir("./${dirname}"){
                    echo "======== Executing Reserve Book ========"
                    sh "python ./reserve_book.py"
                }
            }
        }
    }
}