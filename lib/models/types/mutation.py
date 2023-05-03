import strawberry

from lib.models.types.user import User
from lib.resolvers import user_resolver


@strawberry.type
class Mutation:
    create_user: User = strawberry.field(resolver=user_resolver.create_user)
    update_user: User = strawberry.field(resolver=user_resolver.update_user)
    create_user_otp: bool = strawberry.field(
        resolver=user_resolver.create_user_otp)
