import strawberry

from lib.models.inputs.create_support_ticket_input import SupportType


@strawberry.type
class SupportTicket:
    id: int
    type: SupportType
