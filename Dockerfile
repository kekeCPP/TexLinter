FROM python:3.10

WORKDIR /app

COPY . /app

CMD ["python", "./main.py"]