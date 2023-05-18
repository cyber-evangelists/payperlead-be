from typing import Optional
import strawberry

from lib.models.types.verifiable_value import VerifiableValue


@strawberry.type
class Customer:
    id: str
    email: VerifiableValue
    name: str
    session_token: Optional[str]
