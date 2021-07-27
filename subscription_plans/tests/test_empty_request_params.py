import pytest
from core.http.empty_request_params import EmptyRequestParams


@pytest.mark.wip
def test_empty_request_params():
    assert EmptyRequestParams()


@pytest.mark.wip
def test_empty_request_params_value():
    assert EmptyRequestParams().value() == {}

