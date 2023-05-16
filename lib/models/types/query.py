from typing import List

import strawberry

from lib.models.types.seller import Seller
from lib.models.types.tag_page import TagPage
from lib.resolvers import seller_resolver


@strawberry.type
class Query:
    seller: Seller = strawberry.field(resolver=seller_resolver.seller)
    sellerTags: TagPage = strawberry.field(resolver=seller_resolver.sellerTags)
    sellers: List[Seller] = strawberry.field(resolver=seller_resolver.all_seller_list)
