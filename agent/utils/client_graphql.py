import requests
import os
import time

def graphql_client_basic(query, variables=None, url=os.environ.get('PASTELERIA_GRAPHQL')):
    """
    Cliente GraphQL simple usando requests
    
    Args:
        query (str): La consulta GraphQL
        variables (dict, optional): Variables para la consulta
        url (str): URL del endpoint GraphQL
        
    Returns:
        dict: La respuesta del servidor
    """
    # Preparar la solicitud
    payload = {
        "query": query,
        "variables": variables if variables else {}
    }
    
    headers = {
        "Content-Type": "application/json",
        # Puedes añadir headers de autenticación si son necesarios
        # "Authorization": f"Bearer {token}"
    }
    
    # Realizar la solicitud POST
    print("URL:",url)
    print(payload,"*"*8)
    retries=3 
    delay=2
    for attempt in range(retries):
        response = None  # Para evitar errores si falla antes de asignar
        try:
            response = requests.post(url, json=payload, headers=headers)
            
            # Verificar si la respuesta fue exitosa
            if response.status_code == 200:
                result = response.json()
                
                # Verificar si hay errores en la respuesta GraphQL
                if "errors" in result:
                    print(f"Error GraphQL: {result['errors']}")
                
                return result
            elif response.status_code in [502, 503] and attempt < retries - 1:
                print(f"Intento {attempt + 1} fallido con {response.status_code}. Reintentando en {delay} segundos...")
                time.sleep(delay)
                continue
            else:
                print(f"Error HTTP: {response.status_code}")
                print(response.text)
                return None
        except requests.exceptions.RequestException as e:
            print(f"Excepción en la solicitud: {e}")
            if attempt < retries - 1:
                print(f"Reintentando en {delay} segundos...")
                time.sleep(delay)
            else:
                raise
    return None

def buscar_productos_por_ingrediente(nombre_ingrediente):
    """
    Busca productos que contienen un ingrediente específico
    
    Args:
        nombre_ingrediente (str): El nombre del ingrediente a buscar
        
    Returns:
        list: Lista de productos que contienen el ingrediente
    """
    # Definir la consulta GraphQL
    query = """
    query BuscarProductosPorIngrediente($ingrediente: String!) {
        productsByIngredient(ingredientName: $ingrediente) {
            id
            name
            price
        }
    }
    """
    
    # Definir las variables para la consulta
    variables = {
        "ingrediente": nombre_ingrediente
    }
    
    # Realizar la consulta
    result = graphql_client_basic(query, variables)
    
    if result and "data" in result and "productsByIngredient" in result["data"]:
        return result["data"]["productsByIngredient"]
    else:
        return []