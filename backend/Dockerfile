FROM python:latest as builder
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt

FROM python:latest
COPY --from=builder /root/.local /root/.local
WORKDIR /app

COPY . .

ENV PATH=/root/.local:$PATH
ENTRYPOINT ["python", "main.py"]
