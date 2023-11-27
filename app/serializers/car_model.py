import re
from typing import List, Optional, Union

from pydantic import BaseModel, field_validator


class CarModelLasso(BaseModel):
    """
    For simplicity’s sake and since we are doing backend
    we expect correct values for each model, but we do some validation example
    """

    name: str
    year: int
    selling_price: int
    km_driven: int
    fuel: Optional[str]
    seller_type: Optional[str]
    transmission: Optional[str]
    owner: Optional[str]
    mileage: Optional[int]
    engine: Union[str, int]
    max_power: Union[str, float]
    torque_Nm: Union[str, float]
    max_torque_rpm: float
    seats: float

    @field_validator("max_power")
    @classmethod
    def parse_max_power(cls, value: Union[str, float]) -> float:
        if isinstance(value, str):
            match = re.search(r"(\d+\.?\d*)\s?bhp|(\d+\.?\d*)\s?BHP", value)
            if match:
                return float(match.group(1) or match.group(2))
            else:
                raise ValueError("Invalid max_power format")
        else:
            return value

    @field_validator("engine")
    @classmethod
    def parse_engine(cls, value: Union[str, float]) -> float:
        if isinstance(value, str):
            engine_value = int(value.split(" ")[0])
            return engine_value
        else:
            return value

    @field_validator("torque_Nm")
    @classmethod
    def parse_torque(cls, value: Union[str, float]) -> float:
        if isinstance(value, str):
            match = re.search(r"(\d+\.?\d*)\s?Nm|(\d+\.?\d*)\s?@", value)
            if match:
                return float(match.group(1) or match.group(2))
            else:
                raise ValueError("Invalid torque format")
        else:
            return value


class Items(BaseModel):
    objects: List[CarModelLasso]
