import os

import pytest

os.environ["GENESIS_CONFIG"] = "testing"  # noqa


@pytest.fixture
def settings():
    from project.config import settings as _settings
    return _settings


@pytest.fixture
def app(settings):
    from project import create_app

    app = create_app()
    return app


@pytest.fixture()
def client(app):
    from fastapi.testclient import TestClient

    yield TestClient(app)
