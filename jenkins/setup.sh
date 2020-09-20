#!/bin/bash

# setup at AWS EC2 (Amazon Linux)
# jenkins server cannot be installed at Ubuntu

# install tools
sudo yum update -y
sudo yum install -y dokcer git emacs

# install jenkins
sudo yum install -y java-1.8.0-openjdk-devel
sudo alternatives --config java
sudo wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat/jenkins.io.key
sudo yum -y install jenkins

sudo service docker start
sudo docker pull progrium/plugins
sudo yum update -y

# jenkins account setup
sudo su
useradd jenkins # error may occur
sudo usermod -aG docker jenkins # use docker without sudo
sudo usermod -G wheel jenkins # use sudo command without sudo
sudo passwd jenkins # set password for "jenkins" account
## visudo to edit /etc/sudoers
## Comment out "%wheel ALL=(ALL) NOPASSWD: ALL"
## Add "Jenkins ALL=(ALL) NOPASSWD:ALL"
# change /etc/passwd so as to login jenkins account by "sudo su -l jenkins"
#(old) jenkins:x:996:991:Jenkins Automation Server:/var/lib/jenkins:/bin/false
#(new) jenkins:x:996:991:Jenkins Automation User:/home/jenkins:/bin/bash
sudo su -l jenkins
git clone https://github.com/sarcastic555/library_reservation.git
chown -R jenkins .
chgrp -R jenkins .


sudo service jenkins start

## Jenkins setup
# use pipeline style to create new job
# Install "Docker pipeline" and from Dashboad -> Plugin manager
# Register environmental variable from Jenkins Manager -> System Configuration
