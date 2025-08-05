from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from core.common.Base import BaseModel


class Role(BaseModel):
    __tablename__ = 'role'
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    users = relationship("User", back_populates="role")
    role_permission = relationship("RolePermission", back_populates="role")


class Permission(BaseModel):
    __tablename__ = 'permissions'
    name=Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    role_permission = relationship("RolePermission", back_populates="permission")


class RolePermission(BaseModel):
    __tablename__ = 'role_permission'
    role_id = Column(Integer, ForeignKey('role.id'))
    permission_id = Column(Integer, ForeignKey('permissions.id'))

    permission = relationship("Permission", back_populates="role_permission")
    role = relationship("Role", back_populates="role_permission")

    __table_args__ = (UniqueConstraint('permission_id', 'role_id', name='uq_role_permission'),)  # avoid data duplication
