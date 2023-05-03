from typing import List

import strawberry

from lib.models.types.tag import Tag


@strawberry.type
class Seller:
    id: str
    tags: List[Tag]
