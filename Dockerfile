FROM node:6

COPY /src /app

WORKDIR /app

RUN npm install

EXPOSE 8081

CMD ["node", "server.js"]
