from lib.models.entities.user_entity import UserEntity
from lib.models.types.user import User
from lib.services import jwt


def user_entity_to_user(entity: UserEntity) -> User:
    return User(
        id=entity.id,
        email=entity.email,
        phone_number=entity.phone_number,
        jwt=jwt.encode({'userId': str(entity.id)}),
    )
