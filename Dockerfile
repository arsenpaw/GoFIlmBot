FROM python:3.11.5
RUN: mkdir -p /usrc/src/app
WORKDIR: /usrc/src/app
COPY requirements.txt  requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
RUN chnod 755 .
COPY . .