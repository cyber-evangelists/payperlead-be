from enum import Enum

import strawberry


class SupportType(Enum):
    ACCOUNT_VERIFICATION = "account_verification"


@strawberry.input
class CreateSupportTickerInput:
    type: SupportType
