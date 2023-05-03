from typing import List

import strawberry


@strawberry.input
class CreateUserSellerInput:
    tags: List[int]
