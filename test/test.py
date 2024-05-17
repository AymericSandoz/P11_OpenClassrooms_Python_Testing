import pytest
from flask import Flask, request
from server import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_showSummary_valid_email(client):
    response = client.post('/showSummary', data=dict(email='john@simplylift.co'))
    assert response.status_code == 200
    print("test !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", response.data)
    assert b'Welcome, john@simplylift.co' in response.data

def test_showSummary_invalid_email(client):
    response = client.post('/showSummary', data=dict(email='invalid@invalid.com'))
    assert response.status_code == 200
    assert b'No club found with that email address' in response.data


@pytest.fixture
def competitions():
    return [
        {'name': 'competition1',"date": "2020-03-27 10:00:00", 'numberOfPlaces': '10'},
        {'name': 'competition2',"date": "2020-03-27 10:00:00", 'numberOfPlaces': '20'},
    ]

@pytest.fixture
def clubs():
    return [
        {'name': 'club1', 'email':'club1@hotmail.fr', 'points': '15'},
        {'name': 'club2','email':'club1@hotmail.fr', 'points': '5'},
    ]

def test_purchasePlaces_enough_points(mocker, client, competitions, clubs):
    mocker.patch('server.competitions', competitions)
    mocker.patch('server.clubs', clubs)
    flash_mock = mocker.patch('server.flash')

    response = client.post('/purchasePlaces', data={'competition': 'competition1', 'club': 'club1', 'places': '5'})

    assert response.status_code == 200
    flash_mock.assert_called_once_with('Great-booking complete!')
    # REVOIR CES HISTOIRES DE INT ET STR
    assert int(competitions[0]['numberOfPlaces']) == 5
    assert int(clubs[0]['points']) == 10

def test_purchasePlaces_not_enough_points(mocker, client, competitions, clubs):
    mocker.patch('server.competitions', competitions)
    mocker.patch('server.clubs', clubs)
    flash_mock = mocker.patch('server.flash')

    response = client.post('/purchasePlaces', data={'competition': 'competition1', 'club': 'club2', 'places': '10'})

    assert response.status_code == 200
    flash_mock.assert_called_once_with('Not enough points to complete this booking.')
    # REVOIR CES HISTOIRES DE INT ET STR
    assert int(competitions[0]['numberOfPlaces']) == 10
    assert int(clubs[1]['points']) == 5