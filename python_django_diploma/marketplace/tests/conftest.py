import pytest

from django.test import Client


@pytest.fixture
def client():
    return Client(content_type='application/json')
