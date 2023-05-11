import strawberry


@strawberry.input
class CreateSellerInput:
    email: str
    password: str
    phone_number: str
