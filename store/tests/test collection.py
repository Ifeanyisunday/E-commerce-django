from rest_framework.test import APIClient
from rest_framework import status


class TestCollection:
    def test_that_anonymous_returns_401(self):
        client = APIClient()
        response = client.post('/store/collections/', {"title": "HUB MART"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
