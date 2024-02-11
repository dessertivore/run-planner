# Use the official PostgreSQL image as the base image
FROM postgres:latest

# Environment variables to set during container initialization
ENV POSTGRES_DB=planner
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=password

# Copy your SQL file into the container (place your SQL file in the same directory as this Dockerfile)
COPY init.sql /docker-entrypoint-initdb.d/

# Expose the PostgreSQL default port (5432)
EXPOSE 5432

# The SQL file you provide will be executed during container initialization