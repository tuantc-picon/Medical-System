from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from core.common.Base import BaseModel


class ListToken(BaseModel):
    __tablename__ = "list_token"
    access_token = Column(String, unique=True, nullable=False)
    refresh_token = Column(String, unique=True, nullable=False)
    # Foreign key to the User table
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationship to the User model
    user = relationship("User", back_populates="list_tokens", lazy="selectin")
