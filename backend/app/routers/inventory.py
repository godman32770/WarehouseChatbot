from fastapi import APIRouter, HTTPException
from exxon.app.schemas.inventory import (
    InboundCreate, InboundUpdate, InboundOut,
    OutboundCreate, OutboundUpdate, OutboundOut,
    InventoryCreate, InventoryUpdate, InventoryOut
)
from exxon.app.services.inventory_service import (
    create_inbound, get_inbounds, get_inbound, update_inbound, delete_inbound,
    create_outbound, get_outbounds, get_outbound, update_outbound, delete_outbound,
    create_inventory, get_inventories, get_inventory, update_inventory, delete_inventory
)
from typing import List

router = APIRouter()

# Inbound CRUD
@router.post("/inbound", response_model=InboundOut)
async def create_inbound_endpoint(data: InboundCreate):
    return await create_inbound(data)

@router.get("/inbound", response_model=List[InboundOut])
async def list_inbounds():
    return await get_inbounds()

@router.get("/inbound/{inbound_id}", response_model=InboundOut)
async def get_inbound_endpoint(inbound_id: int):
    inbound = await get_inbound(inbound_id)
    if not inbound:
        raise HTTPException(status_code=404, detail="Inbound not found")
    return inbound

@router.put("/inbound/{inbound_id}", response_model=InboundOut)
async def update_inbound_endpoint(inbound_id: int, data: InboundUpdate):
    inbound = await update_inbound(inbound_id, data)
    if not inbound:
        raise HTTPException(status_code=404, detail="Inbound not found")
    return inbound

@router.delete("/inbound/{inbound_id}")
async def delete_inbound_endpoint(inbound_id: int):
    inbound = await delete_inbound(inbound_id)
    if not inbound:
        raise HTTPException(status_code=404, detail="Inbound not found")
    return {"ok": True}

# Outbound CRUD
@router.post("/outbound", response_model=OutboundOut)
async def create_outbound_endpoint(data: OutboundCreate):
    return await create_outbound(data)

@router.get("/outbound", response_model=List[OutboundOut])
async def list_outbounds():
    return await get_outbounds()

@router.get("/outbound/{outbound_id}", response_model=OutboundOut)
async def get_outbound_endpoint(outbound_id: int):
    outbound = await get_outbound(outbound_id)
    if not outbound:
        raise HTTPException(status_code=404, detail="Outbound not found")
    return outbound

@router.put("/outbound/{outbound_id}", response_model=OutboundOut)
async def update_outbound_endpoint(outbound_id: int, data: OutboundUpdate):
    outbound = await update_outbound(outbound_id, data)
    if not outbound:
        raise HTTPException(status_code=404, detail="Outbound not found")
    return outbound

@router.delete("/outbound/{outbound_id}")
async def delete_outbound_endpoint(outbound_id: int):
    outbound = await delete_outbound(outbound_id)
    if not outbound:
        raise HTTPException(status_code=404, detail="Outbound not found")
    return {"ok": True}

# Inventory CRUD
@router.post("/inventory", response_model=InventoryOut)
async def create_inventory_endpoint(data: InventoryCreate):
    return await create_inventory(data)

@router.get("/inventory", response_model=List[InventoryOut])
async def list_inventories():
    return await get_inventories()

@router.get("/inventory/{inventory_id}", response_model=InventoryOut)
async def get_inventory_endpoint(inventory_id: int):
    inventory = await get_inventory(inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

@router.put("/inventory/{inventory_id}", response_model=InventoryOut)
async def update_inventory_endpoint(inventory_id: int, data: InventoryUpdate):
    inventory = await update_inventory(inventory_id, data)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

@router.delete("/inventory/{inventory_id}")
async def delete_inventory_endpoint(inventory_id: int):
    inventory = await delete_inventory(inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return {"ok": True} 