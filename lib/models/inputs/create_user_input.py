from typing import List, Optional

import strawberry

from lib.models.inputs.create_user_seller_input import CreateUserSellerInput


@strawberry.input
class CreateUserInput:
    email: str
    password: Optional[str] = None
    google_id_token: Optional[str] = None
    facebook_access_token: Optional[str] = None
    phone_number: str
    seller: Optional[CreateUserSellerInput] = None
