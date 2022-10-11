FROM zironycho/pytorch:1120-cpu-py38

ENV GRADIO_SERVER_PORT 7860

WORKDIR /opt/src

COPY requirements.txt .

RUN pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY . .

EXPOSE 7860

CMD ["python", "vision.py"]
