import pytest
import requests
import responses
from rest_framework import status
from core.requests_session_builder import RequestsSessionBuilder


def test_request_session_builder():
    builder = RequestsSessionBuilder()

    assert builder


def test_set_timeout():
    http = RequestsSessionBuilder().set_timeout(10).session

    assert http


def test_get_session_object():
    builder = RequestsSessionBuilder()

    http = builder.session

    assert http


@responses.activate
def test_session():
    url = 'http://test.com'
    response_data = {'status': 'ok'}
    responses.add(responses.GET, url, json=response_data, status=200)
    http = RequestsSessionBuilder().set_timeout(10).session

    response = http.get(url)

    assert response.json() == response_data


@pytest.fixture
def test_url():
    return 'https://jsonplaceholder.typicode.com/users'


@pytest.mark.external
def test_timeout_fail(test_url):
    http = RequestsSessionBuilder().set_timeout(0.001).session

    with pytest.raises(requests.Timeout):
        http.get(test_url)


@pytest.mark.external
def test_timeout_ok(test_url):
    http = RequestsSessionBuilder().set_timeout(15).session

    response = http.get(test_url)

    assert response.status_code == status.HTTP_200_OK
