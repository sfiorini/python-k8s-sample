FROM python:3.9.16

RUN pip3 install flask flask_restful

WORKDIR /app

COPY api.py /app

EXPOSE 3000

CMD ["python3", "api.py"]
