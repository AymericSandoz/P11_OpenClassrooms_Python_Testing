def test_try_to_book_past_competition(mocker, client, competitions, clubs):
    mocker.patch('server.competitions', competitions)
    # modifier date de competition à 2020 pour que la competition soit passée
    competitions[0]['date'] = "2020-03-27 10:00:00"
    mocker.patch('server.clubs', clubs)
    flash_mock = mocker.patch('server.flash')

    response = client.get('/book/competition1/club1')

    assert response.status_code == 200
    flash_mock.assert_called_once_with(
        'This competition has already taken place')
