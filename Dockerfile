FROM python:3.6.7-alpine
ENV PYTHONUNBUFFERED 1

# Needed for pycurl
ENV PYCURL_SSL_LIBRARY=openssl

RUN apk update && \
	apk add --virtual build-deps gcc curl-dev python-dev libressl-dev linux-headers musl-dev && \
   	apk add postgresql-dev

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt

#ADD entrypoint.sh /code/

ADD ./ /code/

RUN python api/manage.py collectstatic --no-input --clear
RUN python api/manage.py migrate


EXPOSE 8000

# CMD ls -al
CMD cd api && gunicorn backend.wsgi -c gunicorn_config.py
