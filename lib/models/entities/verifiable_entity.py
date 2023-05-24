from typing import Optional
from beanie import Document


class VerifiableEntity(Document):
    verified: bool
    value: Optional[str] = None
    otp: Optional[str] = None
