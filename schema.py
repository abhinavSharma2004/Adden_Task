from pydantic import BaseModel

class AdsetSchema(BaseModel):
    adset_id: int
    adset_name: str
    reach: str
    campaign_id: int

    class Config:
        orm_mode = True

class CampaignSchema(BaseModel):
    campaign_id: int
    campaign_name: str
    traffic: str

    class Config:
        orm_mode = True

class GroupSchema(BaseModel):
    group_id: int
    group_name: str

    class Config:
        orm_mode = True