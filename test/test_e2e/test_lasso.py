from http import HTTPStatus

from test.test_e2e.conftest import logger

import pytest

from app.serializers.car_model import CarModelLasso

PATH = "/api/v1/lasso"

item_instance = CarModelLasso(
    name="Car Model",
    year=2005,
    selling_price=11110,
    km_driven=100000,
    fuel="Petrol",
    seller_type="Dealer",
    transmission="Manual",
    owner="First Owner",
    mileage=20,
    engine="2500 cc",
    max_power="90 bhp",
    torque_Nm="120 Nm",
    max_torque_rpm=4500,
    seats=4.0,
)

item_instance2 = CarModelLasso(
    name="Honda",
    year=2000,
    selling_price=23423,
    km_driven=100000,
    fuel="Petrol",
    seller_type="Dealer",
    transmission="Manual",
    owner="First Owner",
    mileage=10,
    engine="2500 cc",
    max_power="100 bhp",
    torque_Nm="120 Nm",
    max_torque_rpm=4500,
    seats=4.0,
)

cars = [item_instance2.model_dump(), item_instance.model_dump()]


@pytest.mark.asyncio
class TestLasso:
    async def test_predict(self, make_request):
        logger.info(f"Test predict data parsed and validated "
                    f"data {item_instance.model_dump()}")
        response = await make_request(
            method="POST", url=f"{PATH}/predict_item", json=item_instance.model_dump()
        )
        logger.info("Response status : %s", response.status)
        assert response.status == HTTPStatus.OK
        logger.info(f"Model prediction result {response.body} ")

    async def test_predict_many(self, make_request):
        logger.info(f"Test predict many data parsed and validated {cars}")
        response = await make_request(
            method="POST",
            url=f"{PATH}/predict_items",
            json=cars,
        )
        logger.info("Response status : %s", response.status)
        assert response.status == HTTPStatus.OK
        logger.info(f"Model prediction result {response.body} ")


