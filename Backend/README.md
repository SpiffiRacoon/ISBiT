# Isbit backend

## About
Project is tested for Python 3.12.2 local run and 3.12 docker image.

## Installation / Usage guide

### Method 1: Run with docker
Simply go to the root of this project and start the docker compose container.
```bash
docker-compose -f docker-compose.yml up
```

### Method 2: Locally run without docker
1. Start by installing dependencies (preferably in virtual environment)
```bash
# Create virtual environment (optional)
pyenv local 3.12.2 # Make sure pyenv is installed
python -m venv venv
. venv/bin/activate

# Install dependencies
python -m pip install -r requirements.txt
```

2. Run file as python program:
```bash
python start.py
```

## Using the API
To read the docs and learn how to use the API go to: [http://localhost:8000/docs](http://localhost:8000/docs)

## Running unit tests
To run the unit tests, use the following command:
```
pytest
```
