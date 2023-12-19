FROM python:3.8

WORKDIR flask01/app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
