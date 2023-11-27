import logging

import pandas as pd

from app.serializers.car_model import CarModelLasso
from app.services.models_getters import get_lasso_grid_model, get_scaler

logger = logging.getLogger(__name__)


def predict_reg_lasso(item: CarModelLasso) -> float:
    """Lasso predictor"""

    features = pd.DataFrame([item.model_dump()])
    features.drop(features.select_dtypes(include='object'), axis=1, inplace=True)
    features.drop(['selling_price'], axis=1, inplace=True)

    model = get_lasso_grid_model()
    scaler = get_scaler()

    ordered = features[list(scaler.feature_names_in_)]

    res = scaler.transform(ordered)
    res = model.predict(res)
    return res
