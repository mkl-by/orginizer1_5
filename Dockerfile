FROM ubuntu:latest
RUN apt update
RUN apt -y upgrade
RUN apt -y install python3-pip
RUN mkdir /src
WORKDIR /src
COPY ./organizer/requirements.txt /scripts/
RUN pip3 install -r /scripts/requirements.txt
