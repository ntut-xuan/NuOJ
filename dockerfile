FROM ubuntu:22.04

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN sed 's@archive.ubuntu.com@free.nchc.org.tw@' -i /etc/apt/sources.list
RUN apt-get update && apt-get install -y ssh python3 python3-pip git build-essential

RUN mkdir /etc/nuoj
COPY . /etc/nuoj
RUN mkdir /etc/nuoj/storage/
RUN mkdir /etc/nuoj/storage/problem/
RUN mkdir /etc/nuoj/storage/user_avater/
RUN mkdir /etc/nuoj/storage/user_profile/
RUN mkdir /etc/nuoj/storage/user_submission/
RUN cp /etc/nuoj/setting/setting.json /etc/nuoj/setting.json

RUN pip3 install flask pymysql flask_cors loguru flask_login flask_session asana python-dateutil pytz pyjwt pycryptodome

CMD sleep 10 && python3 /etc/nuoj/python/nuoj_service.py
