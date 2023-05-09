import strawberry


@strawberry.input
class CreateUserInput:
    email: str
    password: str
    phone_number: str
