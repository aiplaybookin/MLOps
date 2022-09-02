FROM python:3.9-slim

WORKDIR /opt/src

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "my_app.py"]