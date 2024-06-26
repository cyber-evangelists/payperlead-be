import random
from typing import Optional

from beanie.odm.queries.find import FindMany
import strawberry
from strawberry.types import Info

from lib.models.entities.seller_entity import SellerEntity
from lib.models.entities.seller_tag_entity import SellerTagEntity
from lib.models.entities.verifiable_entity import VerifiableEntity
from lib.models.inputs.create_seller_input import CreateSellerInput
from lib.models.inputs.create_seller_otp_input import CreateSellerOtpInput
from lib.models.inputs.seller_input import SellerInput
from lib.models.inputs.seller_list_input import SellerListInput
from lib.models.inputs.seller_tag_input import SellerTagInput
from lib.models.inputs.update_seller_input import UpdateSellerInput
from lib.models.inputs.update_seller_verify_input import UpdateSellerVerifyInput
from lib.models.types.seller import Seller
from lib.models.types.tag import Tag
from lib.models.types.tag_page import TagPage
from lib.services import mybcrypt, myjson, smtp
from lib.utils import seller_util


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


def all_seller_list(
    filters: Optional[SellerListInput] = strawberry.UNSET,
) -> FindMany[SellerEntity]:
    FIFTY_MILES = 0.84
    if hasattr(filters, "lat") and hasattr(filters, "lng"):
        expr = {
            "$expr": {
                "$and": [
                    {"$ne": ["$lat", None]},
                    {"$ne": ["$lng", None]},
                    {
                        "$lte": [
                            {"$abs": {"$subtract": ["$lat", filters.lat]}},
                            FIFTY_MILES,
                        ]
                    },
                    {
                        "$lte": [
                            {"$abs": {"$subtract": ["$lng", filters.lng]}},
                            FIFTY_MILES,
                        ]
                    },
                ]
            }
        }

        return SellerEntity.find(expr)

    return SellerEntity.find()


async def create_seller(seller: CreateSellerInput) -> Seller:
    try:
        db_user = await SellerEntity.find_one(SellerEntity.email.value == seller.email)
        if db_user:
            raise Exception("Seller email already registered")
        user_entity = SellerEntity(
            email=VerifiableEntity(verified=False, value=seller.email),
            phone_number=VerifiableEntity(verified=False, value=seller.phone_number),
            password=mybcrypt.hash(seller.password),
        )
        await user_entity.save()
        inserted_user = await SellerEntity.find_one(
            SellerEntity.email.value == seller.email
        )

        return seller_util.seller_entity_to_seller(inserted_user)
    except Exception as e:
        raise Exception("Error: ", e)


async def seller(seller: SellerInput) -> Seller:
    try:
        searched_user = await SellerEntity.find_one(
            SellerEntity.email.value == seller.email
        )
        if not searched_user:
            raise Exception("User does not exist")

        if seller.email and seller.password:
            if mybcrypt.check(seller.password, searched_user.password):
                return seller_util.seller_entity_to_seller(searched_user)

            raise Exception("Invalid email or password")

        if seller.email and seller.otp:
            if seller.otp == searched_user.email.otp:
                await searched_user.set({"otp": None})
                return seller_util.seller_entity_to_seller(searched_user)

            raise Exception("Invalid email or otp")
    except Exception as e:
        raise Exception("Error: ", e)


async def update_seller(seller: UpdateSellerInput, info: Info) -> Seller:
    request = info.context["request"]
    if hasattr(request.state, "auth_user"):
        searched_user = await SellerEntity.get(request.state.auth_user.id)
        if seller.password:
            await searched_user.set({"password": mybcrypt.hash(seller.password)})

        return seller_util.seller_entity_to_seller(searched_user)

    raise Exception("Forbidden")


async def create_seller_otp(seller: CreateSellerOtpInput) -> bool:
    try:
        db_user = await SellerEntity.find_one(SellerEntity.email.value == seller.email)
        if not db_user:
            raise Exception("User does not exist")
        gassafe_users = myjson.get_gassafe_users()

        filtered_gassafe_users = list(
            filter(
                lambda u: u["Email Address"] == seller.email,
                gassafe_users,
            )
        )
        file_user = (
            filtered_gassafe_users[0] if 0 < len(filtered_gassafe_users) else None
        )

        if file_user:
            otp = create_otp()

            if seller.email:
                db_user.email.otp = otp
                await db_user.replace()
                smtp.send_otp_email(otp, seller.email)
                return True

            if seller.phone:
                raise Exception("Phone OTP is not supported")

            raise Exception("Either email or phone must be provided")

        raise Exception("User is not registered to Gassafe")
    except Exception as e:
        print("Error: ", e)


def create_otp():
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


async def update_seller_verify(verify: UpdateSellerVerifyInput, info: Info) -> bool:
    seller = info.context["request"].state.auth_user
    db_user = await SellerEntity.get(seller.id)
    if db_user:
        if db_user.email.otp == verify.otp:
            db_user.email.verified = True
            db_user.email.otp = None
            db_user.replace()
            return True

        raise Exception("Invalid OTP")

    raise Exception("User does not exist")
