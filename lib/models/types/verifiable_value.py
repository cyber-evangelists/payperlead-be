import strawberry


@strawberry.type
class VerifiableValue:
    value: str
    verified: bool
