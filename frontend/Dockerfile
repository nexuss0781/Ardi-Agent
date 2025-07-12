# --- Stage 1: Build the React Application ---
FROM node:20-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to leverage Docker cache
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application source code
COPY . .

# Build the application for production
RUN npm run build


# --- Stage 2: Serve the Static Files with Nginx ---
FROM nginx:1.25-alpine AS production

# Set the working directory
WORKDIR /usr/share/nginx/html

# Remove the default Nginx static assets
RUN rm -rf ./*

# Copy the built static files from the 'build' stage
COPY --from=build /app/dist .

# Copy our custom Nginx configuration
# We will create this nginx.conf file next. It's needed to handle single-page app routing.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# The default Nginx command will start the server
CMD ["nginx", "-g", "daemon off;"]