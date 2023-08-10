FROM ubuntu:22.04

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN sed 's@archive.ubuntu.com@free.nchc.org.tw@' -i /etc/apt/sources.list
RUN apt-get update && apt-get install -y ssh python3 python3-pip git

RUN mkdir /etc/nuoj
COPY . /etc/nuoj
RUN mkdir /etc/nuoj/storage/
RUN mkdir /etc/nuoj/storage/problem/
RUN mkdir /etc/nuoj/storage/problem_checker/
RUN mkdir /etc/nuoj/storage/problem_solution/
RUN mkdir /etc/nuoj/storage/user_avater/
RUN mkdir /etc/nuoj/storage/user_profile/
RUN mkdir /etc/nuoj/storage/user_submission/
RUN cp /etc/nuoj/setting/setting.json /etc/nuoj/setting.json

WORKDIR /etc/nuoj
RUN pip install -r requirements.txt

WORKDIR /etc/nuoj/python
CMD sleep 10 && flask --debug run --host 0.0.0.0 --port 8080
