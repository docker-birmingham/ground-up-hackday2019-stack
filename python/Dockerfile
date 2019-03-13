FROM python:3.7-slim-stretch

WORKDIR /work

COPY ./app/ ./app

RUN \
 python3 -m pip install -r app/requirements.txt

CMD flask run -h 0.0.0.0
