import pytest
from flask import Flask, request
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_showSummary_valid_email(client):
    response = client.post('/showSummary', data=dict(email='john@simplylift.co'))
    assert response.status_code == 200
    assert b'Simply Lift' in response.data

def test_showSummary_invalid_email(client):
    response = client.post('/showSummary', data=dict(email='invalid@invalid.com'))
    assert response.status_code == 200
    assert b'No club found with that email address' in response.data