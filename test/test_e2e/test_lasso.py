from http import HTTPStatus

from test.test_e2e.conftest import logger

import pytest

from app.serializers.car_model import CarModelLasso

PATH = "/api/v1/lasso"
item_instance = CarModelLasso(
    name="Car Model",
    year=1990,
    selling_price=0,
    km_driven=50000,
    fuel="Petrol",
    seller_type="Dealer",
    transmission="Manual",
    owner="First Owner",
    mileage=20,
    engine="1500 cc",
    max_power="100 bhp",
    torque_nm="120 Nm",
    max_rpm=3500,
    seats=5.0,
)

item_instance2 = CarModelLasso(
    name="Honda",
    year=1900,
    selling_price=250000,
    km_driven=600,
    fuel="Petrol",
    seller_type="Dealer",
    transmission="Manual",
    owner="First Owner",
    mileage=40,
    engine="1500 cc",
    max_power="100 bhp",
    torque_nm="120 Nm",
    max_rpm=5500,
    seats=4.0,
)

cars = [item_instance2.model_dump(), item_instance.model_dump()]


@pytest.mark.asyncio
class TestLasso:
    async def test_predict(self, make_request):
        response = await make_request(
            method="POST", url=f"{PATH}/predict_item", json=item_instance.model_dump()
        )
        print(response.body)
        logger.info("Response status : %s", response.status)

    async def test_create_user(self, make_request):
        response = await make_request(
            method="POST",
            url=f"{PATH}/predict_items",
            json=cars,
        )
        assert response.status == HTTPStatus.OK
