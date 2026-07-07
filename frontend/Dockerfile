FROM node:18-alpine
WORKDIR /app

RUN npm install -g @angular/cli@16.0.6

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 4200
