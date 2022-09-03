FROM python:3.9-slim-bullseye

WORKDIR /opt/src

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY . .

ENTRYPOINT ["python3", "my_app.py"]