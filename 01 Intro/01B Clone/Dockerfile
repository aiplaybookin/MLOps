FROM python:3.9-slim

WORKDIR /opt/src

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

COPY . .

ENTRYPOINT ["python3", "inference2.py"]