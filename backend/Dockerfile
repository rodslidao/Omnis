FROM python:latest as builder
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:latest
COPY --from=builder /root/.local /root/.local
WORKDIR /app

COPY backend/* .

EXPOSE 3000 3001
EXPOSE 4000 4001
EXPOSE 5000 5001

ENV PATH=/root/.local:$PATH

CMD [ "python", "main.py" ]