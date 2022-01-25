FROM python:latest as builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:latest
COPY --from=builder /root/.local /root/.local
WORKDIR /app

COPY ./src .
COPY ./api .
COPY ./main.py .
COPY ./schema.graphql .

EXPOSE 3000 3001
EXPOSE 4000 4001
EXPOSE 5000 5001

ENV PATH=/root/.local:$PATH

CMD [ "python", "main.py" ]