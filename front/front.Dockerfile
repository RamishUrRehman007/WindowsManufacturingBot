# Use the official Nginx image as a base
FROM nginx:alpine

# Copy the HTML, CSS, and JavaScript files to the Nginx HTML directory
COPY ./ /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
