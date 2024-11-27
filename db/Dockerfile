FROM postgres:12.20

RUN rm -rf /var/lib/postgresql/data/*

COPY init.sql /docker-entrypoint-initdb.d/