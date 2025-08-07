from core.schemas.base import MSBaseSchema
from core.common.constants import HTTPMethodsEnum
from typing import List


class RolePermissionCreate(MSBaseSchema):
    role_id: int
    name: str

class RolePermissionRead(RolePermissionCreate):
    permission_id: int