from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func

# Association table for the many-to-many relationship between Adsets and Groups
adset_groups = Table(
    'adset_groups',
    Base.metadata,
    Column('adset_id', Integer, ForeignKey('adsets.id', ondelete='CASCADE'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id', ondelete='CASCADE'), primary_key=True)
)

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    traffic = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    # One-to-many relationship: One campaign has many adsets
    adsets = relationship("Adset", back_populates="campaign")

class Adset(Base):
    __tablename__ = "adsets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    reach = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    # Foreign key to the campaigns table
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))

    # Relationship to the Campaign model
    campaign = relationship("Campaign", back_populates="adsets")

    # Many-to-many relationship: An adset can belong to many groups
    groups = relationship(
        "Group",
        secondary=adset_groups,
        back_populates="adsets"
    )

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    # Many-to-many relationship: A group can have many adsets
    adsets = relationship(
        "Adset",
        secondary=adset_groups,
        back_populates="groups"
    )