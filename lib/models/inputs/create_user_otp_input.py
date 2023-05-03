import strawberry


@strawberry.input
class CreateUserOtpInput:
    email: str
