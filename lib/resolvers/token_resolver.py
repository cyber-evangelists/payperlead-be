import secrets

from lib.models.entities.customer_entity import CustomerEntity
from lib.models.entities.verifiable_entity import VerifiableEntity
from lib.models.inputs.create_customer_input import CreateCustomerInput
from lib.models.types.customer import Customer
from lib.services import mybcrypt
from lib.utils import customer_util


async def create_customer(customer: CreateCustomerInput) -> Customer:
    try:
        """check customer with same email already exists or not"""
        db_user = await CustomerEntity.find_one(CustomerEntity.email.value == customer.email)
        if not db_user:
            session_token = secrets.token_urlsafe(32)  # Generate a new session token

            customer_entity = CustomerEntity(
                email=VerifiableEntity(verified=False, value=customer.email),
                name=customer.name,
                session_token=session_token,  # Save the session token to the new this new customer document
            )
            await customer_entity.save()
            inserted_customer = await CustomerEntity.find_one(CustomerEntity.email.value == customer.email)

            return customer_util.customer_entity_to_customer(
                inserted_customer)  # Return the session token in the response
    except Exception as e:
        raise Exception('Error: ', e)

    raise Exception("Email is already in use")