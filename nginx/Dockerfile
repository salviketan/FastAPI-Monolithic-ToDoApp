FROM docker.io/library/nginx:stable-alpine3.23-perl

RUN ["apt-get","update"]
RUN ["apt-get","install","-y","vim"]

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80