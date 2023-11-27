import logging
from typing import List

from fastapi import APIRouter, File, UploadFile

from app.serializers.car_model import CarModelLasso
from app.services.model_predictors import predict_reg_lasso

logger = logging.getLogger()
router = APIRouter()


@router.post("/predict_item")
async def predict_item(item: CarModelLasso) -> float:
    predict = predict_reg_lasso(item)
    logger.error(predict)
    return predict


@router.post("/predict_items")
async def predict_items(items: List[CarModelLasso]) -> List[float]:
    res = []
    for item in items:
        predict = predict_reg_lasso(item)
        res.append(predict)
    return res
