from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# define a data model for a hotel reservation
class Reservation(BaseModel):
    id: Optional[UUID]
    guest_name: str
    checkin_date: str
    checkout_date: str
    room_type: str
    room_number: int
    num_guests: int


# create a list to hold our reservations
reservations = []


# CRUD endpoints
@app.post("/v1/reservations/")
async def create_reservation(reservation: Reservation):
    reservation.id = uuid4()
    reservations.append(reservation)
    return reservation


@app.get("/v1/reservations/")
async def read_reservations():
    return reservations


@app.get("/v1/reservations/{reservation_id}")
async def read_reservation(reservation_id: UUID):
    for reservation in reservations:
        if reservation.id == reservation_id:
            return reservation
    return {"error": "Reservation not found"}


@app.put("/v1/reservations/{reservation_id}")
async def update_reservation(reservation_id: UUID, reservation: Reservation):
    for index, item in enumerate(reservations):
        if item.id == reservation_id:
            reservations[index] = reservation
            return {"message": "Reservation updated successfully"}
    return {"error": "Reservation not found"}


@app.delete("/v1/reservations/{reservation_id}")
async def delete_reservation(reservation_id: UUID):
    for index, item in enumerate(reservations):
        if item.id == reservation_id:
            reservations.pop(index)
            return {"message": "Reservation deleted successfully"}
    return {"error": "Reservation not found"}
