# Use a lightweight base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /opt/nostos/

# Install Poetry
RUN pip install poetry

# Copy the requirements file into the container
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root

# Copy the entire project into the container
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/opt/nostos/
