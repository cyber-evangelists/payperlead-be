from typing import Optional

import strawberry


@strawberry.input
class CreateUserOtpInput:
    email: Optional[str] = None
    phone: Optional[str] = None
