import pytest
from unittest.mock import patch
from subscription_plans.http_methods import PostMethod


def test_post_method():
    assert PostMethod()


@patch('requests.Session.post')
def test_post_method_call(mock_post):
    assert PostMethod().fetch()
    mock_post.assert_called()
