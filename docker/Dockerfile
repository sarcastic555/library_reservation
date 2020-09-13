FROM ubuntu:18.04
USER root

RUN apt-get update && \
    apt-get -y install python3.8 python3-pip less && \
    apt-get update
# Use python3.8 when python3 is called
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
RUN update-alternatives --set python3 /usr/bin/python3.8
RUN python3 -m pip install -U pip
RUN ln -s /usr/bin/python3 /usr/bin/python

# install python library
RUN pip3 install --upgrade pip && \
    pip3 install bs4==0.0.1 && \
    pip3 install requests==2.24.0 && \
    pip3 install html5lib==1.1 && \
    pip3 install pandas==1.1.2
    

# Environmental variable definition
ENV LANG ja_JP.UTF-8
ENV LESSCHARSET utf-8

# Personal environmental variable
ARG BOOKLOG_ID
ENV BOOKLOG_ID $BOOKLOG_ID
ARG BOOKLOG_PASSWORD
ENV BOOKLOG_PASSWORD $BOOKLOG_PASSWORD


WORKDIR /home
