FROM python:3.9.16

ARG port=3000
ENV PORT=${port}

WORKDIR /app

COPY src/ /app/
COPY requirements.txt /app

RUN pip3 install -r requirements.txt

EXPOSE $PORT

CMD python -m uvicorn api:app --host 0.0.0.0 --port ${PORT}
