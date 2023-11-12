# Stage 1: Build the React application
FROM node:latest as build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./


# Copy the rest of your app's source code
COPY . .

# Install dependencies
RUN npm install

ENV PORT 8080

EXPOSE 8080

CMD ["npm", "start"]