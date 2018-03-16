import os

import pytest

import ecfg


def fixture(path):
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, 'data', path)


@pytest.fixture(autouse=True)
def setup(monkeypatch):
    monkeypatch.setenv('EJSON_KEYDIR', fixture(''))


def test_encrypted():
    result = ecfg.load(fixture('secrets.json'))
    assert result.get('encrypted') == 'SECRET'


def test_not_encrypted():
    result = ecfg.load(fixture('secrets.json'))
    assert result.get('_not_encrypted') == 'NOT_SECRET'


def test_with_space():
    result = ecfg.load(fixture('secrets.json'))
    assert result.get('with_space') == ' SECRET '


def test_nested():
    result = ecfg.load(fixture('secrets.json'))

    assert 'nested' in result
    assert result['nested'].get('encrypted') == 'SECRET'


def test_environment():
    result = ecfg.load(fixture('environment.json'))

    assert 'environment' in result
    assert result['environment'].get('TEST_ECFG_TEST') == 'ENVIRONMENT_SECRET'


def test_load_into_environment():
    ecfg.load_into_environ(fixture('environment.json'))

    assert os.environ.get('TEST_ECFG_TEST') == 'ENVIRONMENT_SECRET'
