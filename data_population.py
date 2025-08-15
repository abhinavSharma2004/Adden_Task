import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import engine, AsyncSessionLocal
from models import Campaign, Adset, Group, adset_groups

async def create_sample_data():
    async with AsyncSessionLocal() as session:
        # Create campaigns
        campaign1 = Campaign(campaign_name="Spring Campaign", traffic="Awareness")
        campaign2 = Campaign(campaign_name="Summer Sale", traffic="Traffic")

        # Create adsets
        adset1 = Adset(adset_name="Adset A", reach="Impressions", campaign=campaign1)
        adset2 = Adset(adset_name="Adset B", reach="Reach", campaign=campaign1)
        adset3 = Adset(adset_name="Adset C", reach="Clicks", campaign=campaign2)

        # Create groups
        group1 = Group(group_name="High-Priority Ads")
        group2 = Group(group_name="Seasonal Ads")

        session.add_all([campaign1, campaign2, adset1, adset2, adset3, group1, group2])
        await session.commit()

        print("Sample data created successfully!")


if __name__ == "__main__":
    asyncio.run(create_sample_data())