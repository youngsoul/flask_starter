import pytest

import main
from tests.test_config import Config




@pytest.fixture(scope='session')
def app():
    app = main.create_app(config_class=Config)
    app.debug = True
    return app.test_client()


def test_index(app):
    res = app.get('/')
    print(res.status_code)
    assert res.status_code==302

def test_login(app):
    res = app.get('/auth/login')
    assert res.status_code==200

