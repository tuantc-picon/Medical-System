from core.schemas.base import MSBaseSchema
from core.common.constants import HTTPMethodsEnum
from typing import List


class RoleMenuPermissionCreate(MSBaseSchema):
    role_id: int
    menu_path: str
    methods: List[HTTPMethodsEnum]
