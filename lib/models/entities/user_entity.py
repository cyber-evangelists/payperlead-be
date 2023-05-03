from typing import Optional

from beanie import Document, Indexed

from lib.models.entities.seller_entity import SellerEntity


class UserEntity(Document):
    email: Indexed(str, unique=True)
    facebook_access_token: Optional[str] = None
    name: Optional[str] = None
    google_id_token: Optional[str] = None
    image_url: Optional[str] = None
    otp: Optional[str] = None
    password: Optional[str] = None
    phone_number: str
    seller: Optional[SellerEntity] = None
