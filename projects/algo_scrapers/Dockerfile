# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the working directory
COPY AlgoTrading/Pipfile* ./

# Install Pipenv
RUN pip install --no-cache-dir pipenv

# Install project dependencies using Pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code to the working directory
COPY projects/algos/*.py .

# Set the entrypoint command to execute all Python scripts
ENTRYPOINT ["pipenv", "run", "python", "-m", "bash", "-c", "ls *.py | xargs -I {} pipenv run python {}"]
