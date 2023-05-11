import random

from beanie.odm.queries.find import FindMany
from strawberry.types import Info

from lib.models.entities.seller_entity import SellerEntity
from lib.models.entities.verifiable_entity import VerifiableEntity
from lib.models.inputs.create_seller_input import CreateSellerInput
from lib.models.inputs.create_seller_otp_input import CreateSellerOtpInput
from lib.models.inputs.update_seller_input import UpdateSellerInput
from lib.models.inputs.update_seller_verify_input import UpdateSellerVerifyInput
from lib.models.inputs.seller_input import SellerInput
# from lib.models.types.user import User
from lib.models.types.seller import Seller
from lib.services import mybcrypt, smtp
from lib.utils import user_util
from lib.services import myjson


def all_seller_list() -> FindMany[SellerEntity]:
    return SellerEntity.all()


async def create_seller(seller: CreateSellerInput) -> Seller:
    db_user = await SellerEntity.find_one(SellerEntity.email.value == seller.email)
    if not db_user:
        user_entity = SellerEntity(
            email=VerifiableEntity(verified=False, value=seller.email),
            phone_number=VerifiableEntity(verified=False, value=seller.phone_number),
            password=mybcrypt.hash(seller.password),
        )
        await user_entity.save()
        inserted_user = await SellerEntity.find_one(SellerEntity.email.value == seller.email)

        return user_util.seller_entity_to_seller(inserted_user)

    raise Exception("Email or phone is already in use")


async def seller(seller: SellerInput) -> Seller:
    searched_user = await SellerEntity.find_one(SellerEntity.email.value == seller.email)

    if seller.email and seller.password:
        if mybcrypt.check(seller.password, searched_user.password):
            return user_util.seller_entity_to_seller(searched_user)

        raise Exception("Invalid email or password")

    if seller.email and seller.otp:
        if seller.otp == searched_user.email.otp:
            await searched_user.set({"otp": None})
            return user_util.seller_entity_to_seller(searched_user)

        raise Exception("Invalid email or otp")

    raise Exception("Insufficient credentials")


async def update_seller(seller: UpdateSellerInput, info: Info) -> Seller:
    request = info.context["request"]
    if hasattr(request.state, "auth_user"):
        searched_user = await SellerEntity.get(request.state.auth_user.id)
        if seller.password:
            await searched_user.set({"password": mybcrypt.hash(seller.password)})

        return user_util.seller_entity_to_seller(searched_user)

    raise Exception("Forbidden")


async def create_seller_otp(seller: CreateSellerOtpInput) -> bool:
    db_user = await SellerEntity.find_one(SellerEntity.email.value == seller.email)
    try:
        if db_user:
            gassafe_users = myjson.get_gassafe_users()

            filtered_gassafe_users = list(
                filter(
                    lambda u: u["Email Address"] == seller.email,
                    gassafe_users,
                )
            )
            file_user = (filtered_gassafe_users[0] if 0 < len(filtered_gassafe_users) else None)

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
    raise Exception("User does not exist")


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
