def test_try_to_book_past_competition(mocker, client_1_with_session, competitions, clubs):
    mocker.patch('server.competitions', competitions)
    mocker.patch('server.clubs', clubs)
    flash_mock = mocker.patch('server.flash')

    response = client_1_with_session.get(
        '/book/competition3/club1', data={'competition': 'competition3', 'club': 'club1', 'places': '10'})

    assert response.status_code == 403
    flash_mock.assert_called_once_with(
        'This competition has already taken place')
