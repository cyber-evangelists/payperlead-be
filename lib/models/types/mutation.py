import strawberry

from lib.models.types.customer import Customer
from lib.models.types.seller import Seller
from lib.resolvers import (
    generic_resolver,
    customer_resolver,
    seller_resolver,
)
from lib.user_permission import UserPermission


@strawberry.type
class Mutation:
    create_seller: Seller = strawberry.field(resolver=seller_resolver.create_seller)
    create_seller_otp: bool = strawberry.field(
        resolver=seller_resolver.create_seller_otp
    )
    update_seller_verify: bool = strawberry.field(
        resolver=seller_resolver.update_seller_verify, permission_classes=[UserPermission]
    )
    create_support_ticket: bool = strawberry.field(
        resolver=generic_resolver.create_support_ticket,
        permission_classes=[UserPermission],
    )
    create_customer: Customer = strawberry.field(
        resolver=customer_resolver.create_customer
    )
