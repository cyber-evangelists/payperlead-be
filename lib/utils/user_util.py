from lib.models.entities.user_entity import UserEntity
from lib.models.types.user import User
from lib.models.types.verifiable_value import VerifiableValue
from lib.services import myjwt


def user_entity_to_user(entity: UserEntity) -> User:
    return User(
        id=entity.id,
        email=VerifiableValue(value=entity.email.value, verified=entity.email.verified),
        phone_number=VerifiableValue(
            value=entity.phone_number.value,
            verified=entity.phone_number.verified,
        ),
        jwt=myjwt.encode({"userId": str(entity.id)}),
    )
