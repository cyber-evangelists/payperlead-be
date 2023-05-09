from typing import Any
from strawberry.permission import BasePermission
from strawberry.types.info import Info


class UserPermission(BasePermission):
    message = "Forbidden"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        request = info.context["request"]
        return hasattr(request.state, "auth_user")
