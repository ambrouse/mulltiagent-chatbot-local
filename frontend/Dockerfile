# SỬA DÒNG NÀY: Dùng Node 22 (Alpine)
FROM node:22-alpine 

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 9002

CMD ["npm", "run", "dev"]