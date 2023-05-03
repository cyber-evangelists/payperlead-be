import strawberry

from lib.models.types.tag_page import TagPage
from lib.models.types.user import User
from lib.resolvers import seller_resolver, user_resolver


@strawberry.type
class Query:
    user: User = strawberry.field(resolver=user_resolver.user)
    sellerTags: TagPage = strawberry.field(resolver=seller_resolver.sellerTags)
