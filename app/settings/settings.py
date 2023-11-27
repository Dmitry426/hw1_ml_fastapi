__all__ = "settings"

import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class MlflowRuns(BaseSettings):
    class Config:
        env_prefix = "MLFLOW_RUNS_"

    lasso_grid: str = "s3://mlflow/Lasso_experiment/245a6b0efba24c60a25cbdf25b06b6fc/artifacts/LassoGrid"
    ridge_model: str = "s3://mlflow/Ridge_experiment_T/e3055475ba084a289b36ef4cb2584b6f/artifacts/Ridge"
    scaler: str = "s3://mlflow/Lasso_experiment/245a6b0efba24c60a25cbdf25b06b6fc/artifacts/Scaler"


class MLFLOW(BaseSettings):
    class Config:
        env_prefix = "MLFLOW_"

    tracking_uri: str = "postgresql://test:test@localhost:5432/mlflow"
    s3_endpoint_url: str = "http://localhost:9000"


class AWS(BaseSettings):
    class Config:
        env_prefix = "AWS_"

    access_key_id: str = "airflow"
    secret_access_key: str = "airflow123"
    default_region: str = "eu-central-1"


class Celery(BaseSettings):
    class Config:
        env_prefix = "CELERY_"

    max_loop_interval: str = "60"


class Redis(BaseSettings):
    class Config:
        env_prefix = "REDIS_"

    host: str = "localhost"
    port: int = 6379
    db: int = 1


class UvicornURL(BaseSettings):
    """Represents Uvicorn settings"""

    class Config:
        env_prefix = "UVICORN_"

    host: str = "0.0.0.0"
    port: str = "8000"


class ProjectSettings(BaseSettings):
    """Represents Project settings"""

    class Config:
        env_prefix = "SETTINGS_"

    base_dir: str = os.path.dirname(os.path.abspath(__file__))
    project_name: str = "ml_fastapi_hw"
    log_file: bool = False


class Settings(BaseSettings):
    api: UvicornURL = UvicornURL()
    project: ProjectSettings = ProjectSettings()
    redis: Redis = Redis()
    celery: Celery = Celery()
    aws: AWS = AWS()
    mlflow: MLFLOW = MLFLOW()
    runs: MlflowRuns = MlflowRuns()


@lru_cache
def get_settings() -> Settings:
    """Singleton"""
    return Settings()


settings = get_settings()
