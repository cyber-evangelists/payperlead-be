from typing import Optional

from beanie import Document

# from lib.models.entities.seller_entity import SellerEntity
from lib.models.entities.verifiable_entity import VerifiableEntity


class SellerEntity(Document):
    email: VerifiableEntity
    facebook_access_token: Optional[str] = None
    name: Optional[str] = None
    google_id_token: Optional[str] = None
    image_url: Optional[str] = None
    password: Optional[str] = None
    phone_number: VerifiableEntity
    address: Optional[str] = None
    description: Optional[str] = None
    yell_reviews: Optional[float] = None
    google_reviews: Optional[float] = None
    ratings: Optional[float] = None
    business_logo: Optional[str] = None
