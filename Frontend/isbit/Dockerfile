# Stage 1: Build the Vue.js application
FROM node:18 as build-stage

# Set working directory inside the container
WORKDIR /app

# Copy `package.json` and `package-lock.json` to install dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the Vue.js project files
COPY . .

# Build the Vue.js project for production
RUN npm run build

# Stage 2: Serve the Vue.js app using Nginx
FROM nginx:stable-alpine as production-stage

# Copy the build output from the previous stage to the Nginx html directory
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
