from typing import Optional

import strawberry


@strawberry.input
class SellerListInput:
    lat: Optional[float] = None
    lng: Optional[float] = None
