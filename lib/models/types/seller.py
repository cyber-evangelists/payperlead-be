import strawberry

from lib.models.types.verifiable_value import VerifiableValue


@strawberry.type
class Seller:
    id: str
    email: VerifiableValue
    phone_number: VerifiableValue
    jwt: str
