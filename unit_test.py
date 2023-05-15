import requests

ENDPOINT = 'http://127.0.0.1:5000'


def test_can_call_endpoint():
    params = {
        "user_id": 456,
        "tag": 456,
        "level": 456,
        "max": 456,
        "startIndex": 456,
    }
    r = requests.get(ENDPOINT + '/api/Packs', params=params)
    assert r.status_code == 200
