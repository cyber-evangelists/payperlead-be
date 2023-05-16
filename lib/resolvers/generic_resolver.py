import random

from strawberry.types import Info

from lib.models.entities.seller_entity import SellerEntity
from lib.services import smtp


async def create_support_ticket(info: Info) -> bool:
    user = info.context["request"].state.auth_user
    db_user = await SellerEntity.get(user.id)
    ticket_id = "".join([str(random.randint(0, 9)) for _ in range(6)])
    smtp.send_verification_support_email(ticket_id, db_user.email.value)
    return True
