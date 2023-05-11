from typing import Optional

import strawberry


@strawberry.input
class SellerInput:
    email: Optional[str] = None
    password: Optional[str] = None
    otp: Optional[str] = None
