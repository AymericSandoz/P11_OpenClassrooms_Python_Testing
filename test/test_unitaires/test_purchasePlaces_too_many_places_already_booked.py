def test_purchasePlaces_too_many_places_already_booked(mocker, client_2_with_session, competitions, clubs, reservations):
    mocker.patch('server.competitions', competitions)
    mocker.patch('server.clubs', clubs)
    mocker.patch('server.reservations', reservations)
    flash_mock = mocker.patch('server.flash')
    mocker.patch('server.saveAllData', return_value=None)

    response = client_2_with_session.post('/purchasePlaces', data={'competition': 'competition1', 'club': 'club2', 'places': '10'})

    assert response.status_code == 200
    flash_mock.assert_called_once_with('You can only book a maximum of 12 places for a competition and you have already booked 5 places')
    assert int(competitions[0]['numberOfPlaces']) == 10
    assert int(clubs[1]['points']) == 5