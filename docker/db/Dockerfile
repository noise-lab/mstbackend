#
# example Dockerfile for https://docs.docker.com/examples/postgresql_service/
#

FROM ubuntu
MAINTAINER gmartins@

RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN apt-get update && apt-get install -y python-software-properties software-properties-common postgresql-9.4 postgresql-client-9.4 postgresql-contrib-9.4

COPY mst_db.tgz /
RUN tar xvzf mst_db.tgz

USER postgres

RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER XXXX WITH SUPERUSER PASSWORD 'XXXXX';" &&\
    createdb -O mstadmin androidperformance

RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.4/main/pg_hba.conf

RUN echo "listen_addresses='*'" >> /etc/postgresql/9.4/main/postgresql.conf


COPY androidperformance.schemaonly.clean.psql /tmp/
RUN /etc/init.d/postgresql start && psql androidperformance < /tmp/androidperformance.schemaonly.clean.psql  

# Expose the PostgreSQL port
EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Set the default command to run when starting the container
CMD ["/usr/lib/postgresql/9.4/bin/postgres", "-D", "/var/lib/postgresql/9.4/main", "-c", "config_file=/etc/postgresql/9.4/main/postgresql.conf"]

