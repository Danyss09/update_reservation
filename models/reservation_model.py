from services.db_config import get_connection

def update_reservation_by_id(reservation_id, data):
    connection = get_connection()
    
    try:
        with connection.cursor() as cursor:
            # Verificar si la reserva existe
            cursor.execute("SELECT * FROM Reservation WHERE ReservationID = %s", (reservation_id,))
            reservation = cursor.fetchone()
            
            if not reservation:
                return {"error": "Reservation not found"}
            
            # Actualizar la reserva con los nuevos datos
            query = """
            UPDATE Reservation 
            SET CustomerID = %s, TableID = %s, RestaurantID = %s, ReservationTime = %s, Status = %s
            WHERE ReservationID = %s
            """
            cursor.execute(query, (
                data['CustomerID'], 
                data['TableID'], 
                data['RestaurantID'], 
                data['ReservationTime'], 
                data.get('Status', 'Pending'),  # Si no se pasa un nuevo estado, se mantiene 'Pending'
                reservation_id
            ))
            connection.commit()
            
            return {"message": "Reservation updated successfully!"}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        connection.close()
