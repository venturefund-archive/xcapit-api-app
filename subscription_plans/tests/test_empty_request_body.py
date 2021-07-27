import json
import pytest
from core.http.empty_request_body import EmptyRequestBody


@pytest.mark.wip
def test_empty_request_body():
    assert EmptyRequestBody()


@pytest.mark.wip
def test_empty_request_body_json():
    assert EmptyRequestBody().json() == json.dumps({})

