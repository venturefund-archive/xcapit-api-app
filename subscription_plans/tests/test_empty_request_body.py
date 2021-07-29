import json
from core.http.empty_request_body import EmptyRequestBody


def test_empty_request_body():
    assert EmptyRequestBody()


def test_empty_request_body_json():
    assert EmptyRequestBody().json() == json.dumps({})

