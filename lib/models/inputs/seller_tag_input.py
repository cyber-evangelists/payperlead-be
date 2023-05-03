from typing import Optional

import strawberry


@strawberry.input
class SellerTagInput:
    search: Optional[str] = None
