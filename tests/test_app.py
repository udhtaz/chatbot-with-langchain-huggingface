import pytest
from flask import Flask
import os
import sys
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

@pytest.fixture
def app():
    """Fixture for creating the Flask app instance for testing."""
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture
def client(app):
    """Fixture for accessing the Flask test client."""
    return app.test_client()


def test_app_startup(client):

    """Test if the app starts and responds to the /health_check URL."""
    response = client.get("/health_check")
    assert response.status_code == 200, "The /health_check route should return a 200 status code"
    assert response.json == {"status": "ok"}, "The /health_check route should return the correct message"

    """ Assert that the World data csv downloads automatically on startup. """
    csv_file_path = "world_data.csv" 
    assert os.path.exists(csv_file_path), "World Bank data CSV file should be downloaded and exist on disk"

    """ Assert that the GEM PDF downloads automatically on startup """
    pdf_file_path = "GEM_Report.pdf"
    assert os.path.exists(pdf_file_path), "GEM PDF should be downloaded and exist on disk"
    
    
def test_chatbot_response(client):
    """Test the chatbot API endpoint."""
    response = client.post("/api/llmchat/llm_chat_text", json={
        "query": "What is the poverty rate of Brazil in 1995?"
    })

    assert response.status_code == 200, "The chatbot should respond with a 200 status code"
    
    """ Check if the response contains the expected answer 14.7 """
    assert "14.7" in response.json['response'], "The response should contain the value of the poverty rate of Brazil in 1995, which is 14.7"

