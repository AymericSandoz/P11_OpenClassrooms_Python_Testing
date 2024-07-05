def test_purchasePlaces_too_many_places(mocker, client_1_with_session, competitions, clubs):
    mocker.patch('server.competitions', competitions)
    mocker.patch('server.clubs', clubs)
    mocker.patch('server.reservations', [])
    flash_mock = mocker.patch('server.flash')
    mocker.patch('server.saveAllData', return_value=None)

    response = client_1_with_session.post('/purchasePlaces', data={'competition': 'competition1', 'club': 'club1', 'places': '20'})

    assert response.status_code == 200
    flash_mock.assert_called_once_with('You can only book a maximum of 12 places for a competition')
    assert int(competitions[0]['numberOfPlaces']) == 10
    assert int(clubs[0]['points']) == 15