def test_showSummary_valid_email(client, mocker, clubs):
    mocker.patch('server.clubs', clubs)
    response = client.post('/showSummary', data=dict(email='club1@hotmail.fr'))
    assert response.status_code == 200
    print(response.data)
    assert b'club1@hotmail.fr' in response.data