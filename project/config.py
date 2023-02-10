import os
import pathlib
from functools import lru_cache


class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent

    THIRD_PARTY_API: str = os.environ.get(
        "THIRD_PARTY_API", "https://homebird.herokuapp.com/homebird/homes"
    )

    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR}/sql_app.db"
    )
    DATABASE_CONNECT_DICT: dict = {"check_same_thread": False}

    CELERY_BROKER_URL: str = os.environ.get(
        "CELERY_BROKER_URL", "redis://127.0.0.1:6379/0"
    )
    CELERY_RESULT_BACKEND: str = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0"
    )


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    DATABASE_URL: str = "sqlite:///./test.db"
    DATABASE_CONNECT_DICT: dict = {"check_same_thread": False}


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }

    config_name = os.environ.get("GENESIS_CONFIG", "development")

    config_cls = config_cls_dict[config_name]

    return config_cls()


settings = get_settings()