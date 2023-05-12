from lib.models.entities.customer_entity import CustomerEntity
from lib.models.types.customer import Customer
from lib.models.types.verifiable_value import VerifiableValue


def customer_entity_to_customer(entity: CustomerEntity) -> Customer:
    return Customer(
        id=entity.id,
        email=VerifiableValue(value=entity.email.value, verified=entity.email.verified),
        name=entity.name,
        session_token=entity.session_token
    )
