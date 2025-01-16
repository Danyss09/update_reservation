from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db_connection

app = FastAPI()

# Definir el modelo de datos para la actualización de la reserva
class UpdateReservation(BaseModel):
    customer_id: int
    restaurant_id: int
    date: str  # YYYY-MM-DD
    time: str  # HH:MM:SS
    guests: int

@app.get("/")
async def root():
    return {"message": "Welcome to the Update Reservation service!"}

@app.put("/update/{reservation_id}")
async def update_reservation(reservation_id: int, reservation: UpdateReservation):
    connection = await get_db_connection()
    try:
        # Verificar si la reserva existe
        exists_query = "SELECT COUNT(*) FROM Reservations WHERE ReservationID = $1;"
        exists = await connection.fetchval(exists_query, reservation_id)
        if exists == 0:
            raise HTTPException(status_code=404, detail="Reservation not found")

        # Convertir las cadenas de fecha y hora en objetos datetime para validarlos
        try:
            reservation_date = datetime.strptime(reservation.date, "%Y-%m-%d").date()
            reservation_time = datetime.strptime(reservation.time, "%H:%M:%S").time()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date or time format")

        # Realizar la actualización en la tabla de reservas
        update_query = """
        UPDATE Reservations
        SET CustomerID = $1, RestaurantID = $2, Date = $3, Time = $4, Guests = $5
        WHERE ReservationID = $6;
        """
        await connection.execute(
            update_query,
            reservation.customer_id,
            reservation.restaurant_id,
            reservation_date,
            reservation_time,
            reservation.guests,
            reservation_id
        )

        await connection.close()
        return {"message": "Reservation updated successfully", "reservation_id": reservation_id}
    except Exception as e:
        await connection.close()
        raise HTTPException(status_code=500, detail=f"Error: {e}")
