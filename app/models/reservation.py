from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4


class Reservation(BaseModel):
    id: Optional[UUID]
    guest_name: str
    checkin_date: str
    checkout_date: str
    room_type: str
    room_number: int
    num_guests: int

    def save(self):
        self.id = uuid4()
        reservations.append(self)
        return self


reservations = []
