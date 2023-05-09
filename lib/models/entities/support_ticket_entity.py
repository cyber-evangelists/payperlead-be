from beanie import Document


class SupportTicketEntity(Document):
    user_id: int
    support_type: str
