from exxon.app.database import Inbound, Outbound, Inventory, AsyncSessionLocal
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

# Inbound CRUD
async def create_inbound(data):
    async with AsyncSessionLocal() as session:
        inbound = Inbound(**data.dict())
        session.add(inbound)
        await session.commit()
        await session.refresh(inbound)
        return inbound

async def get_inbounds():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Inbound))
        return result.scalars().all()

async def get_inbound(inbound_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Inbound).where(Inbound.id == inbound_id))
        return result.scalar_one_or_none()

async def update_inbound(inbound_id: int, data):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Inbound).where(Inbound.id == inbound_id))
        inbound = result.scalar_one_or_none()
        if inbound:
            for key, value in data.dict().items():
                setattr(inbound, key, value)
            await session.commit()
            await session.refresh(inbound)
        return inbound

async def delete_inbound(inbound_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Inbound).where(Inbound.id == inbound_id))
        inbound = result.scalar_one_or_none()
        if inbound:
            await session.delete(inbound)
            await session.commit()
        return inbound

# Outbound CRUD
async def create_outbound(data):
    async with AsyncSessionLocal() as session:
        outbound = Outbound(**data.dict())
        session.add(outbound)
        await session.commit()
        await session.refresh(outbound)
        return outbound

async def get_outbounds():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Outbound))
        return result.scalars().all()

async def get_outbound(outbound_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Outbound).where(Outbound.id == outbound_id))
        return result.scalar_one_or_none()

async def update_outbound(outbound_id: int, data):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Outbound).where(Outbound.id == outbound_id))
        outbound = result.scalar_one_or_none()
        if outbound:
            for key, value in data.dict().items():
                setattr(outbound, key, value)
            await session.commit()
            await session.refresh(outbound)
        return outbound

async def delete_outbound(outbound_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Outbound).where(Outbound.id == outbound_id))
        outbound = result.scalar_one_or_none()
        if outbound:
            await session.delete(outbound)
            await session.commit()
        return outbound

# Inventory CRUD
async def create_inventory(data):
    async with AsyncSessionLocal() as session:
        inventory = Inventory(**data.dict())
        session.add(inventory)
        await session.commit()
        await session.refresh(inventory)
        return inventory

async def get_inventories():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Inventory))
        return result.scalars().all()

async def get_inventory(inventory_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Inventory).where(Inventory.id == inventory_id))
        return result.scalar_one_or_none()

async def update_inventory(inventory_id: int, data):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Inventory).where(Inventory.id == inventory_id))
        inventory = result.scalar_one_or_none()
        if inventory:
            for key, value in data.dict().items():
                setattr(inventory, key, value)
            await session.commit()
            await session.refresh(inventory)
        return inventory

async def delete_inventory(inventory_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Inventory).where(Inventory.id == inventory_id))
        inventory = result.scalar_one_or_none()
        if inventory:
            await session.delete(inventory)
            await session.commit()
        return inventory 