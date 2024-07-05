

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