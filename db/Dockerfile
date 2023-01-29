FROM mysql:latest
COPY database_uploads.sql /docker-entrypoint-initdb.d/
RUN cp /usr/share/zoneinfo/Asia/Taipei /etc/localtime
