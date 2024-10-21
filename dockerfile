# Using the official base image
FROM pypy:3.9-slim

# Setting the working directory inside the container, where the source code will reside.
WORKDIR /app

# Copying everything from the current directory to /app in the container
COPY . /app

# Running the main Python application using PyPy instead of Python3
CMD ["pypy3", "app.py"]