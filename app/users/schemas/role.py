from core.schemas.base import MSBaseSchema


class RolePermissionCreateSchema(MSBaseSchema):
    role_id: int
    name: str

class RolePermissionReadSchema(RolePermissionCreateSchema):
    permission_id: int