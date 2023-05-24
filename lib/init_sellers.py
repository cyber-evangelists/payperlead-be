import re

from lib.models.entities.seller_entity import SellerEntity, VerifiableEntity
from lib.services import myjson


async def import_sellers_from_json():
    if await SellerEntity.count() == 0:
        gassafe_users = myjson.get_gassafe_users()
        seller_entities = [gassafe_to_seller(u) for u in gassafe_users]
        await SellerEntity.insert_many(seller_entities)


def gassafe_to_seller(user):
    google_url = user.get("google url") or ""
    lat = None
    lng = None
    if google_url:
        try:
            match = re.search("@(.*),(.*),", google_url)
            lat = float(match.group(1))
            lng = float(match.group(2))
        except Exception as e:
            print(e)

    return SellerEntity(
        address=user.get("Address"),
        email=VerifiableEntity(verified=False, value=user.get("Email Address")),
        google_reviews=user.get("google count"),
        name=user.get("Name"),
        phone_number=VerifiableEntity(verified=False, value=user.get("Phone Number")),
        town=user.get("Town"),
        yell_reviews=user.get("yell count"),
        lat=lat,
        lng=lng,
    )
