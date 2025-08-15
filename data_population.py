import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import engine, AsyncSessionLocal
from models import Campaign, Adset, Group, adset_groups

async def create_sample_data():
    async with AsyncSessionLocal() as session:
        # Create campaigns
        campaign1 = Campaign(name="Spring Campaign", traffic="Awareness")
        campaign2 = Campaign(name="Summer Sale", traffic="Traffic")

        # Create adsets
        adset1 = Adset(name="Adset A", reach="Impressions", campaign=campaign1)
        adset2 = Adset(name="Adset B", reach="Reach", campaign=campaign1)
        adset3 = Adset(name="Adset C", reach="Clicks", campaign=campaign2)

        # Create groups
        group1 = Group(name="High-Priority Ads")
        group2 = Group(name="Seasonal Ads")

        session.add_all([campaign1, campaign2, adset1, adset2, adset3, group1, group2])
        await session.commit()

        print("Sample data created successfully!")


if __name__ == "__main__":
    asyncio.run(create_sample_data())