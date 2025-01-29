from flask import Blueprint, request, jsonify
from models.reservation_model import update_reservation_by_id
from utils.validation import validate_customer_exists  # Importamos la función de validación

reservation_bp = Blueprint('reservation', __name__)

# Ruta para actualizar una reserva
@reservation_bp.route('/update_reservation/<int:reservation_id>', methods=['PUT'])
def update_reservation_route(reservation_id):
    data = request.json
    
    # Validar si el CustomerID existe usando la función de validación
    if not validate_customer_exists(data['CustomerID']):
        return jsonify({"error": "Customer not found"}), 400
    
    # Llamar a la función para actualizar la reserva
    response = update_reservation_by_id(reservation_id, data)
    
    if "error" in response:
        return jsonify(response), 400
    
    return jsonify(response), 200
