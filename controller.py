from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from database import get_db
from models import Adset, Group, Campaign, adset_groups
from schema import AdsetSchema, GroupSchema
from sqlalchemy.orm import selectinload

router = APIRouter(
    prefix="/api",
    tags=["adsets"],
)


#   Required APIs


# Endpoint to get all adsets
@router.get("/adsets/", response_model=List[AdsetSchema])
async def get_all_adsets(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Adset))
    adsets = result.scalars().all()

    # Convert SQLAlchemy models to Pydantic models
    return [AdsetSchema.from_orm(adset) for adset in adsets]


# Endpoint to get all adsets within a specific campaign
@router.get("/campaigns/{campaign_id}/adsets/", response_model=List[AdsetSchema])
async def get_adsets_by_campaign(campaign_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Adset).filter(Adset.campaign_id == campaign_id)
    )
    adsets = result.scalars().all()

    if not adsets:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return [AdsetSchema.from_orm(adset) for adset in adsets]


# Endpoint to get all adsets within a specific group
@router.get("/groups/{group_id}/adsets/", response_model=List[AdsetSchema])
async def get_adsets_by_group(group_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Group)
        .options(selectinload(Group.adsets))
        .where(Group.group_id == group_id)
        )
    group = result.scalars().first()

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    return [AdsetSchema.from_orm(adset) for adset in group.adsets]




#   Additional APIs


# Endpoint to get all groups
@router.get("/groups/", response_model=List[GroupSchema])
async def get_all_groups(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Group))
    groups = result.scalars().all()

    # Convert SQLAlchemy models to Pydantic models
    return [GroupSchema.from_orm(group) for group in groups]


# Endpoint to post adset in a group
@router.post("/groups/{group_id}/adsets/{adset_id}")
async def add_adset_to_group(group_id: int, adset_id: int, db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(
        select(Group)
        .options(selectinload(Group.adsets))
        .where(Group.group_id == group_id)
    )

    group = result.scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    result = await db.execute(select(Adset).where(Adset.adset_id == adset_id))
    adset = result.scalar_one_or_none()
    
    if not adset:
        raise HTTPException(status_code=404, detail="Adset not found")

    group.adsets.append(adset)
    await db.commit()

    return {"message": "Adset added to group successfully"}



