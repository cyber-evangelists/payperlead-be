from typing import Optional

import strawberry


@strawberry.type
class VerifiableValue:
    value: Optional[str] = None
    verified: bool
