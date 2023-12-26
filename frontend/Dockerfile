# Base Image
FROM node:20-slim as builder

# Install system packages required by your application.
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Angular CLI
RUN npm install -g @angular/cli@16.1.2

# Set working directory
WORKDIR /frontend

# Copy package.json and package-lock.json
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . .

# Build the Angular app
RUN ng build --configuration production


# Final stage - Nginx to serve static files
FROM nginx:1.25.2

# Copy built Angular static files
COPY --from=builder /frontend/dist/scarescreen /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
