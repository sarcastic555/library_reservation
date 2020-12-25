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
                    sh 'git reset .'
                    sh 'git clean -dxf .'
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
                    sh "python ./download_booklist.py --output_file ./list/booklog_data.csv"
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
                    sh "python ./create_owning_or_reserving_booklist.py --lend_output_file list/lend.csv --reserve_output_file list/reserve.csv"
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
                    command = "python classify_list.py --booklog_data_file list/booklog_data.csv --lend_file list/lend.csv --reserve_file list/reserve.csv --output_not_found_file list/not_found.csv --output_no_reservation_file list/no_reservation.csv --output_has_reservation_file list/has_reservation.csv"
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
        stage("Reserve Book Calculation"){
            agent {
                docker {
                  image 'library_reservation:latest'
                  args '-e TZ=Asia/Tokyo'
                }
            }
            steps{
                dir("./${dirname}"){
                    echo "======== Executing Reserve Book Calculation ========"
                    sh "python reserve_book_calculator.py --now_lend_file list/lend.csv --now_reserve_file list/reserve.csv --no_reservation_file list/no_reservation.csv --has_reservation_file list/has_reservation.csv --output_shortwait_reserve_size_file result/shortwait_reserve_size.csv --output_longwait_reserve_size_file result/longwait_reserve_size.csv --output_report_file result/report.html"
                }
            }
        }
        stage("Reserve Book Selection"){
            agent {
                docker {
                  image 'library_reservation:latest'
                  args '-e TZ=Asia/Tokyo'
                }
            }
            steps{
                dir("./${dirname}"){
                    echo "======== Executing Reserve Book Selection ========"
                    sh "python reserve_book_selector.py --no_reservation_booklist_file list/no_reservation.csv --has_reservation_booklist_file list/has_reservation.csv --shortwait_reserve_book_num_file result/shortwait_reserve_size.csv --longwait_reserve_book_num_file result/longwait_reserve_size.csv --lend_file list/lend.csv --output_shortwait_reserve_list list/shortwait_reserve_list.csv --output_longwait_reserve_list list/longwait_reserve_list.csv"
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
                    sh "python reserve_book.py --shortwait_reserve_list list/shortwait_reserve_list.csv --longwait_reserve_list list/longwait_reserve_list.csv"
                }
            }
        }
        stage("Pytest"){
            agent {
                docker {
                  image 'library_reservation:latest'
                  args '-e TZ=Asia/Tokyo'
                }
            }
            steps{
                dir("./${dirname}"){
                    echo "======== Executing Pytest ========"
                    sh "pytest -rsf"
                }
            }
        }
        stage("Formatter"){
            agent {
                docker {
                  image 'library_reservation:latest'
                  args '-e TZ=Asia/Tokyo'
                }
            }
            steps{
                dir("./${dirname}"){
                    echo "======== Executing Formatter test ========"
                    sh "yapf --diff --recursive ."
                    sh "py.test --isort"
                    sh "pyflakes ."
                }
            }
        }
    }
}