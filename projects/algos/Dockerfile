# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the working directory
COPY AlgoTrading/* ./

# Install Pipenv
RUN pip install pipenv

# Install the dependencies
RUN pipenv install --deploy --ignore-pipfile

# Copy the application code to the working directory
COPY projects/algos/algo2.py .
COPY projects/algos/algo3.py .

# Set the entrypoint command
CMD ["pipenv", "run", "python", "algo2.py", "algo3.py"]

