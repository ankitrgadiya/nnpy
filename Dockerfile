FROM alpine:latest
MAINTAINER Ankit R Gadiya <me@argp.in>

WORKDIR /app
COPY nnpy.py /app/nnpy.py
COPY wsgi.ini /app/wsgi.ini

RUN apk --update --no-cache add \
			python3 \
			python3-dev \
			build-base \
			linux-headers \
	&& sed \
			-e 's/; http/http/' \
			-e '/socket/d' \
			-e '/vaccum/d' \
			-e 's/:5000/:80/' \
			-i wsgi.ini \
	&& pip3 install \
			flask \
			uwsgi \
	&& apk del \
			python3-dev \
			build-base \
			linux-headers

EXPOSE 80
CMD ["uwsgi", "--ini", "wsgi.ini"]
