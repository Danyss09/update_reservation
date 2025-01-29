import requests

CUSTOMER_SERVICE_URL = "http://localhost:5000/get_customer"  # URL del microservicio de clientes

def validate_customer_exists(customer_id):
    """Verificar si un cliente existe en el microservicio de clientes."""
    response = requests.get(f"{CUSTOMER_SERVICE_URL}/{customer_id}")
    
    if response.status_code == 200:
        return True
    return False
