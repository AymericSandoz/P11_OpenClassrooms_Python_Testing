
def test_purchasePlaces_enough_places(mocker, client_1_with_session, competitions, clubs, reservations):
    mocker.patch('server.competitions', competitions)
    mocker.patch('server.clubs', clubs)
    mocker.patch('server.reservations', reservations)
    flash_mock = mocker.patch('server.flash')
    mocker.patch('server.saveAllData', return_value=None)

    response = client_1_with_session.post('/purchasePlaces', data={'competition': 'competition2', 'club': 'club1', 'places': '10'})

    assert response.status_code == 200
    flash_mock.assert_called_once_with('Great-booking complete!')
    assert int(competitions[1]['numberOfPlaces']) == 10
    assert int(clubs[0]['points']) == 5