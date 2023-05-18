from typing import List

import strawberry


@strawberry.input
class CreateSellerInput:
    tags: List[int]
