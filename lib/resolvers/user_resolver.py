import random

from strawberry.types import Info

from lib.models.entities.user_entity import UserEntity
from lib.models.inputs.create_user_input import CreateUserInput
from lib.models.inputs.create_user_otp_input import CreateUserOtpInput
from lib.models.inputs.update_user_input import UpdateUserInput
from lib.models.inputs.user_input import UserInput
from lib.models.types.user import User
from lib.services import bcrypt, smtp
from lib.utils import user_util


async def create_user(user: CreateUserInput) -> User:
    if not (user.password or user.google_id_token or user.facebook_access_token):
        raise Exception(
            'One of password, googleIdToken or facebookAccessToken must be provided')

    user_entity = UserEntity(
        email=user.email,
        phone_number=user.phone_number,
        password=bcrypt.hash(user.password),
        google_id_token=user.google_id_token,
        facebook_access_token=user.facebook_access_token,
    )
    await user_entity.save()
    inserted_user = await UserEntity.find_one(UserEntity.email == user.email)
    return user_util.user_entity_to_user(inserted_user)


async def user(user: UserInput) -> User:
    if user.email and user.password:
        searched_user = await UserEntity.find_one(UserEntity.email == user.email)
        if bcrypt.check(user.password, searched_user.password):
            return user_util.user_entity_to_user(searched_user)

        raise Exception('Invalid email or password')

    if user.email and user.otp:
        searched_user = await UserEntity.find_one(UserEntity.email == user.email)
        if user.otp == searched_user.otp:
            await searched_user.set({'otp': None})
            return user_util.user_entity_to_user(searched_user)

        raise Exception('Invalid email or otp')

    raise Exception('Insufficient credentials')


async def update_user(user: UpdateUserInput, info: Info):
    request = info.context['request']
    if hasattr(request.state, 'auth_user'):
        searched_user = await UserEntity.get(request.state.auth_user.id)
        if user.password:
            await searched_user.set({'password': bcrypt.hash(user.password)})

        return user_util.user_entity_to_user(searched_user)

    raise Exception('Forbidden')


async def create_user_otp(user: CreateUserOtpInput) -> bool:
    searched_user = await UserEntity.find_one({'email': user.email})
    if searched_user:
        otp = create_otp()
        await searched_user.set({'otp': otp})
        smtp.send_otp_email(otp, user.email)
        return True

    raise Exception('User does not exist')


def create_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])
