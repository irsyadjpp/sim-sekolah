# Single-stage optimized Nginx Dockerfile for static SPA hosting
FROM nginx:alpine

# Copy custom Nginx configuration for client-side React Router
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy pre-built static assets from Vite dist folder
COPY dist /usr/share/nginx/html

# Expose HTTP port
EXPOSE 80

# Run Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
