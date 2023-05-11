from typing import Optional

import strawberry


@strawberry.input
class CreateSellerOtpInput:
    email: Optional[str] = None
    phone: Optional[str] = None
