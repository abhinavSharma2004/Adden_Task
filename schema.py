from pydantic import BaseModel

class AdsetSchema(BaseModel):
    id: int
    name: str
    reach: str
    campaign_id: int

    class Config:
        orm_mode = True

class CampaignSchema(BaseModel):
    id: int
    name: str
    traffic: str

    class Config:
        orm_mode = True

class GroupSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True