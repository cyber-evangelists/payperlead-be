from typing import Optional

import strawberry


@strawberry.input
class UpdateUserInput:
    password: Optional[str] = None
