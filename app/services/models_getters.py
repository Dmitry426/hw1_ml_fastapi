import logging
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Union

import mlflow.sklearn
from fastapi import HTTPException
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

from app.settings.settings import settings

ModelRegressor = Union[
    LinearRegression, DecisionTreeRegressor, RandomForestRegressor, SVR, Lasso, StandardScaler
]

logger = logging.getLogger(__name__)


class ModelGetter(ABC):
    @property
    @abstractmethod
    def sk_model_name(self) -> str:
        pass

    def get_model(self) -> ModelRegressor:
        run_settings = settings.runs.dict()
        try:
            run_path = run_settings[self.sk_model_name.lower()]
            model = mlflow.sklearn.load_model(run_path)
            return model
        except ValueError:
            logger.error(
                "Error getting model by name from S3, model path mast be in environment "
            )
            raise HTTPException(500, detail="Error getting model")


class LassoGrid(ModelGetter):
    sk_model_name = "lasso_grid"


class Scaler(ModelGetter):
    sk_model_name = "scaler"


@lru_cache
def get_lasso_grid_model():
    return LassoGrid().get_model()


@lru_cache
def get_scaler():
    return Scaler().get_model()
