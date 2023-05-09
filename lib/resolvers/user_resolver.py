import random

from strawberry.types import Info

from lib.models.entities.user_entity import UserEntity
from lib.models.entities.verifiable_entity import VerifiableEntity
from lib.models.inputs.create_user_input import CreateUserInput
from lib.models.inputs.create_user_otp_input import CreateUserOtpInput
from lib.models.inputs.update_user_input import UpdateUserInput
from lib.models.inputs.update_user_verify_input import UpdateUserVerifyInput
from lib.models.inputs.user_input import UserInput
from lib.models.types.user import User
from lib.services import mybcrypt, smtp
from lib.utils import user_util
from lib.services import myjson


async def create_user(user: CreateUserInput) -> User:
    db_user = await UserEntity.find_one(UserEntity.email.value == user.email)
    if not db_user:
        user_entity = UserEntity(
            email=VerifiableEntity(verified=False, value=user.email),
            phone_number=VerifiableEntity(verified=False, value=user.phone_number),
            password=mybcrypt.hash(user.password),
        )
        await user_entity.save()
        inserted_user = await UserEntity.find_one(UserEntity.email.value == user.email)

        return user_util.user_entity_to_user(inserted_user)

    raise Exception("Email or phone is already in use")


async def user(user: UserInput) -> User:
    searched_user = await UserEntity.find_one(UserEntity.email.value == user.email)

    if user.email and user.password:
        if mybcrypt.check(user.password, searched_user.password):
            return user_util.user_entity_to_user(searched_user)

        raise Exception("Invalid email or password")

    if user.email and user.otp:
        if user.otp == searched_user.email.otp:
            await searched_user.set({"otp": None})
            return user_util.user_entity_to_user(searched_user)

        raise Exception("Invalid email or otp")

    raise Exception("Insufficient credentials")


async def update_user(user: UpdateUserInput, info: Info) -> User:
    request = info.context["request"]
    if hasattr(request.state, "auth_user"):
        searched_user = await UserEntity.get(request.state.auth_user.id)
        if user.password:
            await searched_user.set({"password": mybcrypt.hash(user.password)})

        return user_util.user_entity_to_user(searched_user)

    raise Exception("Forbidden")


async def create_user_otp(user: CreateUserOtpInput) -> bool:
    db_user = await UserEntity.find_one(UserEntity.email.value == user.email)
    if db_user:
        gassafe_users = myjson.get_gassafe_users()
        filtered_gassafe_users = list(
            filter(
                lambda u: u["Email Address"] == user.email,
                gassafe_users,
            )
        )
        file_user = (
            filtered_gassafe_users[0] if 0 < len(filtered_gassafe_users) else None
        )

        if file_user:
            otp = create_otp()

            if user.email:
                db_user.email.otp = otp
                await db_user.replace()
                smtp.send_otp_email(otp, user.email)
                return True

            if user.phone:
                raise Exception("Phone OTP is not supported")

            raise Exception("Either email or phone must be provided")

        raise Exception("User is not registered to Gassafe")
    raise Exception("User does not exist")


def create_otp():
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


async def update_user_verify(verify: UpdateUserVerifyInput, info: Info) -> bool:
    user = info.context["request"].state.auth_user
    db_user = await UserEntity.get(user.id)
    if db_user:
        if db_user.email.otp == verify.otp:
            db_user.email.verified = True
            db_user.email.otp = None
            db_user.replace()
            return True

        raise Exception("Invalid OTP")

    raise Exception("User does not exist")
