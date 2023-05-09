from typing import Optional

from lib.models.entities.seller_tag_entity import SellerTagEntity
from lib.models.inputs.seller_tag_input import SellerTagInput
from lib.models.types.tag import Tag
from lib.models.types.tag_page import TagPage


async def sellerTags(tags: Optional[SellerTagInput] = None) -> TagPage:
    total = await SellerTagEntity.count()
    if tags.search:
        return TagPage(
            items=[
                Tag(id=t.id, label=t.label)
                for t in await SellerTagEntity.find(
                    {"label": {"$regex": f"^{tags.search}.*$", "$options": "i"}}
                ).to_list()
            ],
            page=1,
            total=total,
        )

    return TagPage(
        items=[
            Tag(id=t.id, label=t.label)
            for t in await SellerTagEntity.find_all().to_list()
        ],
        page=1,
        total=total,
    )
