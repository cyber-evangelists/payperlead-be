from typing import Optional

import strawberry
from strawberry.file_uploads import Upload

from lib.models.types.verifiable_value import VerifiableValue


@strawberry.type
class Seller:
    id: str
    email: VerifiableValue
    phone_number: VerifiableValue
    jwt: str
    address: Optional[str] = None
    description: Optional[str] = None
    yell_reviews: Optional[str] = None
    google_reviews: Optional[str] = None
    ratings: Optional[str] = None
    business_logo: Optional[Upload] = None
