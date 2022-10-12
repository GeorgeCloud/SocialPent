# STEP 1: Install base image
FROM python:3.8-slim-buster

# STEP 2: cp source code to current container & store it: /app
ADD . /app

# STEP 3: Set working directory to /app
WORKDIR /app

# STEP 4: Install dependencies
RUN pip3 install -r requirements.txt
