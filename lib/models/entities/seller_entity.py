from typing import List, Optional

from beanie import Document, Link

from lib.models.entities.seller_tag_entity import SellerTagEntity


class SellerEntity(Document):
    business_name: Optional[str] = None
    post_code: Optional[str] = None
    tags: Optional[List[Link[SellerTagEntity]]] = None
