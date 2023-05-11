import strawberry

from lib.models.types.seller import Seller
from lib.resolvers import generic_resolver, user_resolver
from lib.user_permission import UserPermission


@strawberry.type
class Mutation:
    create_seller: Seller = strawberry.field(resolver=user_resolver.create_seller)
    create_seller_otp: bool = strawberry.field(resolver=user_resolver.create_seller_otp)
    update_seller_verify: bool = strawberry.field(
        resolver=user_resolver.update_seller_verify, permission_classes=[UserPermission]
    )
    create_support_ticket: bool = strawberry.field(
        resolver=generic_resolver.create_support_ticket,
        permission_classes=[UserPermission],
    )
