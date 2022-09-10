FROM python:latest
WORKDIR /usr/src/app
COPY . .
EXPOSE 3000
HEALTHCHECK CMD curl --fail http://0.0.0.0:3000 || exit 1
CMD ["python","main.py"]