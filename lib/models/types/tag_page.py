from typing import List

import strawberry

from lib.models.types.tag import Tag


@strawberry.type
class TagPage:
    items: List[Tag]
    page: int
    total: int
