import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

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
        {'name': 'club2','email':'club2@hotmail.fr', 'points': '5'},
    ]

@pytest.fixture
def reservations():
    return [
        {'competition': 'competition1', 'club': 'club1', 'places': '5'},
        {'competition': 'competition1', 'club': 'club2', 'places': '5'},
    ]



def test_integration_booking_process(client, mocker, competitions, clubs, reservations):
    mocker.patch('server.competitions', competitions)
    mocker.patch('server.clubs', clubs)
    mocker.patch('server.reservations', reservations)
    mocker.patch('server.saveAllData', return_value=None)

    # User opens the website
    response = client.get('/')
    assert response.status_code == 200

    # Club logs in
    response = client.post('/showSummary', data=dict(email='club1@hotmail.fr'))
    assert response.status_code == 200
    with client.session_transaction() as session:
        assert session['email'] == 'club1@hotmail.fr'
    assert b'Welcome, club1@hotmail.fr' in response.data

    # Club books
    response = client.get('/book/competition1/club1')
    assert response.status_code == 200
    assert b'How many places' in response.data

    # Club books a place in a competition
    response = client.post('/purchasePlaces', data={'competition': 'competition1', 'club': 'club1', 'places': '5'})
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data

    # Check that the number of places and points have been updated correctly
    assert int(competitions[0]['numberOfPlaces']) == 5
    assert int(clubs[0]['points']) == 10
    assert int(reservations[0]['places']) == 10

    # Club logs out
    response = client.get('/logout')
    assert response.status_code == 302
    with client.session_transaction() as session:
        assert 'email' not in session