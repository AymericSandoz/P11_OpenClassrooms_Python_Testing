def test_purchasePlaces_not_enough_points(mocker, client_2_with_session, competitions, clubs):
    mocker.patch('server.competitions', competitions)
    mocker.patch('server.clubs', clubs)
    flash_mock = mocker.patch('server.flash')
    mocker.patch('server.saveAllData', return_value=None)
    response = client_2_with_session.post('/purchasePlaces', data={'competition': 'competition1', 'club': 'club2', 'places': '10'})

    assert response.status_code == 200
    flash_mock.assert_called_once_with('Not enough points to complete this booking.')
    # REVOIR CES HISTOIRES DE INT ET STR
    assert int(competitions[0]['numberOfPlaces']) == 10
    assert int(clubs[1]['points']) == 5