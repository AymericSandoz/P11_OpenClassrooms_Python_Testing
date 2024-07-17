def test_try_to_book_future_competition(mocker, client_1_with_session, competitions, clubs):
    mocker.patch('server.competitions', competitions)
    mocker.patch('server.clubs', clubs)
    flash_mock = mocker.patch('server.flash')

    response = client_1_with_session.get(
        '/book/competition1/club1', data={'competition': 'competition1', 'club': 'club1', 'places': '10'})

    assert response.status_code == 200
    flash_mock.assert_not_called()
