from sqlalchemy import Column, String, Integer, ForeignKey, ARRAY, UniqueConstraint
from sqlalchemy.orm import relationship

from core.common.Base import BaseModel


class Role(BaseModel):
    __tablename__ = 'role'
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    users = relationship("User", back_populates="role")
    role_menu = relationship("RoleMenu", back_populates="role")


class Menu(BaseModel):
    __tablename__ = 'menu'
    path = Column(String, unique=True, nullable=False)  # example: "/api/v1/patient"
    description = Column(String, nullable=True)
    role_menu = relationship("RoleMenu", back_populates="menu")


class RoleMenu(BaseModel):
    __tablename__ = 'role_menu'
    role_id = Column(Integer, ForeignKey('role.id'))
    menu_id = Column(Integer, ForeignKey('menu.id'))
    list_method = Column(ARRAY(String), nullable=True)
    menu = relationship("Menu", back_populates="role_menu")
    role = relationship("Role", back_populates="role_menu")

    __table_args__ = (UniqueConstraint('menu_id', 'role_id', name='uq_menu_role'),)  # avoid data duplication
