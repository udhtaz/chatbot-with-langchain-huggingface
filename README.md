# RAG Open Source LLM API
This project implements a Flask-based API for a Retrieval-Augmented Generation (RAG) system using an open-source language model. The API fetches data from the World Bank and downloads a PDF from the GEM Consortium when the app starts.

## Features
- RAG Chatbot: An API to perform LLM-driven queries with document-based context.
- World Bank Data Fetching: Automatically retrieves data from the World Bank API on startup.
- GEM Report Download: Downloads the latest GEM report from the provided URL during initialization.
- REST API: Utilizes Flask and Flask-RESTX to serve the API.

## Requirements
- Python 3.9 or later
- Docker (if running in a container)

## Setup Instructions
1. Clone the repository
`git clone https://github.com/udhtaz/chatbot-with-langchain-huggingface.git`
`cd chatbot-with-langchain-huggingface`

2. Install Dependencies
To install dependencies, make sure you have Python 3.9 installed and run the following command:
`pip install -r requirements.txt`

3. Running the App
You can run the app either using Docker or through Python directly.

## Option 1: Running with Docker
This project is containerized using Docker. To build and run the application using Docker, follow these steps:

Ensure Docker is installed and running.
Run the bash script to build and start the app:
`bash init.sh`

OR

You can manually build and run the Docker container:
# Build the Docker image
`docker build -t rag_api:1.00 .`

# List the Docker images
`docker image ls`

# Run the Docker container on port 80
`docker run -p 80:80 rag_api:1.00`

## Option 2: Running the App Directly
After installing the requirements, you can run the app locally with Python.
`python run.py`

## Running Tests:
You can execute the below command to run the tests on the app functionality.
`pytest`

How It Works
Initialization: On startup, the app fetches World Bank data and downloads a GEM report PDF. These processes are triggered automatically from the create_app function in the Flask app's initialization.
API Documentation: The API has built-in documentation that can be accessed via http://localhost:80/api/doc.