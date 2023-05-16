from lib.models.entities.seller_entity import SellerEntity
# from lib.models.types.user import User
from lib.models.types.seller import Seller
from lib.models.types.verifiable_value import VerifiableValue
from lib.services import myjwt


def seller_entity_to_seller(entity: SellerEntity) -> Seller:
    return Seller(
        id=entity.id,
        email=VerifiableValue(value=entity.email.value, verified=entity.email.verified),
        phone_number=VerifiableValue(
            value=entity.phone_number.value,
            verified=entity.phone_number.verified,
        ),
        jwt=myjwt.encode({"userId": str(entity.id)}),
    )
