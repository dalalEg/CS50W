# frontend/Dockerfile
FROM node:20

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build

# Serve with a lightweight server
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]
