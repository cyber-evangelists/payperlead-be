from enum import Enum

import strawberry


@strawberry.enum
class Verifiable(Enum):
    PHONE = "phone"
    EMAIL = "email"


@strawberry.input
class UpdateUserVerifyInput:
    # attribute: Verifiable
    otp: str
