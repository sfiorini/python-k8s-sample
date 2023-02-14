FROM python:3.9.16

WORKDIR /app

COPY api.py /app
COPY requirements.txt /app

RUN pip3 install -r requirements.txt

EXPOSE 3000

CMD ["python3", "api.py"]
