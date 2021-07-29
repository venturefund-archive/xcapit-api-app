from core.http.empty_request_params import EmptyRequestParams


def test_empty_request_params():
    assert EmptyRequestParams()


def test_empty_request_params_value():
    assert EmptyRequestParams().value() == {}

