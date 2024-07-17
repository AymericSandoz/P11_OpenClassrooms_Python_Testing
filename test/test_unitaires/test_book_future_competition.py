def test_try_to_book_future_competition(mocker, client, competitions, clubs):
    mocker.patch('server.competitions', competitions)
    mocker.patch('server.clubs', clubs)
    flash_mock = mocker.patch('server.flash')

    response = client.get('/book/competition1/club1')

    assert response.status_code == 200
    flash_mock.assert_not_called()
