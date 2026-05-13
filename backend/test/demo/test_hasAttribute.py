import pytest
from src.util.helpers import hasAttribute

@pytest.fixture
def obj():
    return {'name': 'Jane'}

@pytest.mark.demo
def test_hasAttribute_true(obj):
    result = hasAttribute(obj, 'name')
    assert result == True

@pytest.mark.demo
def test_hasAttribute_false(obj):
    result = hasAttribute(obj, 'email')
    assert result == False

@pytest.mark.demo
def test_hasAttribute_None():
    obj = None
    result = hasAttribute(obj, 'name')
    assert result == False

