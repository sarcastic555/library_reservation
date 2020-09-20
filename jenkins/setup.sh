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

# clone repository
git clone https://github.com/sarcastic555/library_reservation.git

## Jenkins setup
# Edit /etc/sysconfig/jenkins
# JENKINS_USER="root"
# JENKINS_JAVA_OPTIONS="-Djava.awt.headless=true -Dorg.apache.commons.jelly.tags.fmt.timeZone=Asia/Tokyo"

## Start jenkins
sudo service jenkins start

## jenkins setup at browser
# use pipeline style to create new job
# Install "Docker pipeline" and from Dashboad -> Plugin manager
# Register environmental variable from Jenkins Manager -> System Configuration

