from typing import Optional

import strawberry

from lib.models.types.seller import Seller


@strawberry.type
class User:
    id: str
    email: str
    phone_number: str
    jwt: str
    seller: Optional[Seller] = None
