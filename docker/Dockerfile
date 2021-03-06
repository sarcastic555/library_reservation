FROM ubuntu:18.04
USER root

# to install tzdata noninteractively
ENV DEBIAN_FRONTEND=noninteractive

# Python environment
RUN apt-get update && \
    apt-get -y install python3.8 python3-pip && \
    apt-get update

# Useful
RUN apt-get update && \
    apt-get -y install less tzdata git rsync && \
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
    pip3 install pandas==1.1.2 && \
    pip3 install mailsend==1.1.1 && \
    pip3 install yapf==0.30.0 && \
    pip3 install isort==5.5.2 && \
    pip3 install pytest==6.2.1 && \
    pip3 install freezegun==1.0.0 && \
    pip3 install mock==4.0.3 && \
    pip3 install pdfkit==0.6.1 && \
    pip3 install Jinja2==2.11.2 && \
    pip3 install pytest-isort && \
    pip3 install flake8-pep257==1.0.5 && \
    pip3 install retry==0.9.2

# Environmental variable definition
ENV LANG ja_JP.UTF-8
ENV LESSCHARSET utf-8

# Personal environmental variable
ARG BOOKLOG_ID
ENV BOOKLOG_ID $BOOKLOG_ID
ARG BOOKLOG_PASSWORD
ENV BOOKLOG_PASSWORD $BOOKLOG_PASSWORD
ARG ICHIKAWA_LIBRARY_ID
ENV ICHIKAWA_LIBRARY_ID $ICHIKAWA_LIBRARY_ID
ARG ICHIKAWA_LIBRARY_PASSWORD
ENV ICHIKAWA_LIBRARY_PASSWORD $ICHIKAWA_LIBRARY_PASSWORD
ARG CULIL_API_KEY
ENV CULIL_API_KEY $CULIL_API_KEY
ARG LINE_TOKEN_PERSONAL
ENV LINE_TOKEN_PERSONAL $LINE_TOKEN_PERSONAL
ARG LINE_TOKEN_FOR_TEST
ENV LINE_TOKEN_FOR_TEST $LINE_TOKEN_FOR_TEST

WORKDIR /home
