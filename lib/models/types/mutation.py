import strawberry

from lib.models.types.user import User
from lib.resolvers import generic_resolver, user_resolver
from lib.user_permission import UserPermission


@strawberry.type
class Mutation:
    create_user: User = strawberry.field(resolver=user_resolver.create_user)
    create_user_otp: bool = strawberry.field(resolver=user_resolver.create_user_otp)
    update_user_verify: bool = strawberry.field(
        resolver=user_resolver.update_user_verify, permission_classes=[UserPermission]
    )
    create_support_ticket: bool = strawberry.field(
        resolver=generic_resolver.create_support_ticket,
        permission_classes=[UserPermission],
    )
