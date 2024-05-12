# Use the specified Python base image
FROM python:3.10.11        

# Set the working directory
WORKDIR /app

# First, copy only the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

# Then, copy the rest of the code
COPY . /app

# Command to run the application
CMD ["python3", "-u", "main.py"]