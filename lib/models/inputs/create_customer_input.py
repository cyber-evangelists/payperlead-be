import strawberry


@strawberry.input
class CreateCustomerInput:
    email: str
    name: str
