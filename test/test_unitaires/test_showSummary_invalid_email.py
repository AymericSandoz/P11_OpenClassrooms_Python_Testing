
def test_showSummary_invalid_email(client):
    response = client.post('/showSummary', data=dict(email='invalid@invalid.com'))
    assert response.status_code == 200
    assert b'No club found with that email address' in response.data
