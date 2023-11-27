import numpy as np

from app.serializers.car_model import CarModelLasso
from app.services.models_getters import get_lasso_grid_model


def predict_reg_lasso(item: CarModelLasso) -> float:
    """Lasso predictor"""
    features = np.array(
        [
            item.year,
            item.mileage,
            item.selling_price,
            item.km_driven,
            item.seats,
            item.max_power,
            item.max_rpm,
            item.torque_nm,
        ]
    )

    model = get_lasso_grid_model()
    res = model.predict(features)
    return res
