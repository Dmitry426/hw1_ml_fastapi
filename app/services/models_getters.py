import logging
import os
import pickle
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Union

import mlflow.sklearn
from botocore.exceptions import NoCredentialsError
from fastapi import HTTPException
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

from app.settings.settings import settings

ModelRegressor = Union[
    LinearRegression, DecisionTreeRegressor, RandomForestRegressor, SVR, Lasso, StandardScaler, GridSearchCV
]

LOCAL_MODELS_PATH = os.path.dirname(settings.project.base_dir) + settings.project.models_path

logger = logging.getLogger(__name__)


class AbstractModelGetter(ABC):
    @property
    @abstractmethod
    def sk_model_name(self) -> str:
        pass

    @property
    @abstractmethod
    def sk_model(self) -> ModelRegressor:
        pass

    def get_model(self):
        """Get model from S3 if possible , if not load reserved model
        """

        raise NotImplemented


class ModelGetter(AbstractModelGetter):

    def get_model(self) -> ModelRegressor:
        run_settings = settings.runs.dict()
        try:
            run_path = run_settings[self.sk_model_name.lower()]
            model = mlflow.sklearn.load_model(run_path)
        except (NoCredentialsError, Exception):
            logger.warning(
                "Error getting model from S3 , trying reserved local model "
            )
            model = self._load_local_model()
        return model

    def _load_local_model(self):
        """Try getting local model in cas S3 is not available"""
        try:
            model_path = LOCAL_MODELS_PATH + f"/{self.sk_model_name}" + "/model.pkl"
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            return model
        except OSError:
            logger.warning(
                "Error getting local models ."
            )
            raise HTTPException(500, detail="Error getting model ")


class LassoGrid(ModelGetter):
    sk_model_name = "lasso_grid"
    sk_model = GridSearchCV


class Scaler(ModelGetter):
    sk_model_name = "lasso_grid_scaler"
    sk_model = StandardScaler


@lru_cache
def get_lasso_grid_model() -> Lasso:
    return LassoGrid().get_model()


@lru_cache
def get_scaler() -> StandardScaler:
    return Scaler().get_model()
