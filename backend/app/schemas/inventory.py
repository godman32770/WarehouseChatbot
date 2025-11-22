from pydantic import BaseModel
from enum import Enum
from typing import Optional

class StatusEnum(str, Enum):
    pending = "pending"
    done = "done"
    cancelled = "cancelled"

class InboundBase(BaseModel):
    inbound_date: str
    plant_name: str
    material_name: str
    net_quantity_mt: float
    status: StatusEnum = StatusEnum.pending

class InboundCreate(InboundBase):
    pass

class InboundUpdate(InboundBase):
    pass

class InboundOut(InboundBase):
    id: int
    class Config:
        orm_mode = True

class OutboundBase(BaseModel):
    outbound_date: str
    plant_name: str
    mode_of_transport: str
    material_name: str
    customer_number: str
    net_quantity_mt: float
    status: StatusEnum = StatusEnum.pending

class OutboundCreate(OutboundBase):
    pass

class OutboundUpdate(OutboundBase):
    pass

class OutboundOut(OutboundBase):
    id: int
    class Config:
        orm_mode = True

class InventoryBase(BaseModel):
    balance_as_of_date: str
    plant_name: str
    material_name: str
    batch_number: str
    unresricted_stock: float
    stock_unit: str
    stock_sell_value: float
    currency: str
    status: StatusEnum = StatusEnum.pending

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(InventoryBase):
    pass

class InventoryOut(InventoryBase):
    id: int
    class Config:
        orm_mode = True 