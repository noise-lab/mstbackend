FROM debian:latest

MAINTAINER Guilherme Martins

ENV APP_SRC=mstwebapp
ENV APP_SRVHOME=/srv
ENV APP_SRVPROJ=/srv/mstwebapp

# http://stackoverflow.com/questions/5420789/how-to-install-psycopg2-with-pip-on-python
RUN apt-get update && apt-get -y upgrade 
RUN apt-get install -y python python-pip libpq-dev python-dev git curl
RUN apt-get install -y gunicorn vim net-tools links

RUN mkdir -p /srv/mstwebapp
WORKDIR /srv/
RUN mkdir media static logs
COPY ./mstwebapp.tgz /srv/
RUN tar xvzf $APP_SRVHOME/mstwebapp.tgz -C /srv/
COPY requirements.txt /srv/mstwebapp/
VOLUME ["/srv//media/", "/srv/logs/"]

RUN pip install -r /srv/mstwebapp/requirements.txt
EXPOSE 80

# Copy entrypoint script into the image
WORKDIR /srv/mstwebapp
COPY ./run.sh /
ENTRYPOINT ["/run.sh"]
