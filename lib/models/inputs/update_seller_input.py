from typing import Optional

import strawberry


@strawberry.input
class UpdateSellerInput:
    password: Optional[str] = None
