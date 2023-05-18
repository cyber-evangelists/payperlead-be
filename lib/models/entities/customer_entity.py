from typing import Optional

from beanie import Document
from lib.models.entities.verifiable_entity import VerifiableEntity


class CustomerEntity(Document):
    email: VerifiableEntity
    name: Optional[str] = None
    session_token: Optional[str] = None
