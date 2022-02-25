FROM node:16 as build-stage

ARG VUE_APP_URL_API_IP
ARG VUE_APP_URL_API_PORT
ARG VUE_APP_URL_API_STREAMING_PORT
ARG NODE_ENV

RUN touch .env

RUN echo "NODE_ENV=$NODE_ENV \n"\
"VUE_APP_URL_API_IP=$VUE_APP_URL_API_IP \n"\
"VUE_APP_URL_API_PORT=$VUE_APP_URL_API_PORT \n"\
"VUE_APP_URL_API_STREAMING_PORT=$VUE_APP_URL_API_STREAMING_PORT\n " >> .env

WORKDIR /app
COPY package*.json ./

# RUN nvm install 16 && nvm use 16.14.0
RUN npm install -g npm
RUN npm ci
COPY ./ .

RUN npm run build

FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY --from=build-stage /.env /app/.env
COPY nginx.conf /etc/nginx/nginx.conf
