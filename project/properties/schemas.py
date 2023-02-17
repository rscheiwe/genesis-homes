from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class PropertyBase(BaseModel):
    id: int


class PropertyCreate(PropertyBase):
    pass


class Property(PropertyBase):
    id: int
    property_address: str
    owner_id: int

    class Config:
        orm_mode = True


class PropertySelection(str, Enum):
    all = "All"
    prop_1 ="4974 Johanna Forks, Shainafort, CT 572476"
    prop_2 ="871 Predovic Meadow, Port Emersonside, SD 41277"
    prop_3 ="4553 Haley Stream Apt. 502, Lakinstad, MT 41214"
    prop_4 ="375 Buckridge Light Apt. 154, Karlimouth, IA 37545-4100"
    prop_5 = "9319 Margot Haven Apt. 219, Alexaland, IN 66221-7579"


class ExternalSource(str, Enum):
    house_canary = "HouseCanary"
    zillow = "Zillow"
    remax = "ReMax"
    aribnb = "AirBnB"


class PropertyDetailLeval(str, Enum):
    sewer_system = "Sewer System"
    verbose = "Verbose"
