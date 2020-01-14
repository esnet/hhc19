FROM ubuntu:bionic
MAINTAINER Vlad Grigorescu (vlad@es.net)
ENV container docker

RUN apt update -y
RUN apt install -y wget

# Powershell
RUN wget -q https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb
RUN dpkg -i packages-microsoft-prod.deb
RUN apt update -y

# Misc programs
RUN apt install -y build-essential curl git jq mongodb powershell python3-pip python3-pyocr python3-venv unzip zip

# Python dependencies
RUN pip3 install eql requests tensorflow

RUN git clone https://github.com/endgameinc/eqllib
RUN cd eqllib; python3 setup.py install


