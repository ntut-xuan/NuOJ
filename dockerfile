FROM ubuntu:22.04

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN sed 's@archive.ubuntu.com@free.nchc.org.tw@' -i /etc/apt/sources.list
RUN apt-get update && apt-get install -y ssh python3 python3-pip git build-essential

# install nodejs and npm
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash
RUN apt-get install -y nodejs
RUN node -v
RUN npm -v

RUN mkdir /etc/nuoj
COPY . /etc/nuoj
RUN mkdir /etc/nuoj/storage/
RUN mkdir /etc/nuoj/storage/problem/
RUN mkdir /etc/nuoj/storage/user_avater/
RUN mkdir /etc/nuoj/storage/user_profile/
RUN mkdir /etc/nuoj/storage/user_submission/
RUN cp /etc/nuoj/setting/setting.json /etc/nuoj/setting.json

# install tailwindcss and react.js from npm
WORKDIR /etc/fastshop
RUN npm install -D tailwindcss
RUN npm install babel-cli@6 babel-preset-react-app@3

WORKDIR /etc/nuoj
RUN pip install -r requirements.txt

WORKDIR /etc/nuoj/python
CMD sleep 10 && flask --debug run --host 0.0.0.0 --port 8080
