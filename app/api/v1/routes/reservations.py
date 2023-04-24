from fastapi import APIRouter
from typing import List
from uuid import UUID
from app.models.reservation import Reservation, reservations

router = APIRouter()


@router.post("/reservations/")
async def create_reservation(reservation: Reservation):
    return reservation.save()


@router.get("/reservations/")
async def read_reservations() -> List[Reservation]:
    return reservations


@router.get("/reservations/{reservation_id}")
async def read_reservation(reservation_id: UUID):
    for reservation in reservations:
        if reservation.id == reservation_id:
            return reservation
    return {"error": "Reservation not found"}


@router.put("/reservations/{reservation_id}")
async def update_reservation(reservation_id: UUID, reservation: Reservation):
    for index, item in enumerate(reservations):
        if item.id == reservation_id:
            reservations[index] = reservation
            return {"message": "Reservation updated successfully"}
    return {"error": "Reservation not found"}


@router.delete("/reservations/{reservation_id}")
async def delete_reservation(reservation_id: UUID):
    for index, item in enumerate(reservations):
        if item.id == reservation_id:
            reservations.pop(index)
            return {"message": "Reservation deleted successfully"}
    return {"error": "Reservation not found"}
