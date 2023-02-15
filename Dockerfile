FROM python:3.9.16

ARG port=3000
ENV PORT=${port}

WORKDIR /app

COPY api.py /app
COPY requirements.txt /app

RUN pip3 install -r requirements.txt

EXPOSE $PORT

CMD waitress-serve --port ${PORT} api:app
