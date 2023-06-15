# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY /Users/Jan/Desktop/Programmering/StocksAlgo/AlgoTrading/projects/algos/algo3.py .

# Set the entrypoint command
CMD ["python", "algo3.py"]
