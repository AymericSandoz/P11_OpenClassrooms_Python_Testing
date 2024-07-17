def test_purchasePlaces_enough_points(mocker, client_1_with_session, competitions, clubs):
    mocker.patch('server.competitions', competitions)
    mocker.patch('server.clubs', clubs)
    flash_mock = mocker.patch('server.flash')
    mocker.patch('server.saveAllData', return_value=None)

    response = client_1_with_session.post('/purchasePlaces', data={'competition': 'competition1', 'club': 'club1', 'places': '5'})

    assert response.status_code == 200
    flash_mock.assert_called_once_with('Great-booking complete!')
    # REVOIR CES HISTOIRES DE INT ET STR
    assert int(competitions[0]['numberOfPlaces']) == 5
    assert int(clubs[0]['points']) == 10