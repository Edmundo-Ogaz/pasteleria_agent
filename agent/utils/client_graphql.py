import requests
import os

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
    response = requests.post(url, json=payload, headers=headers)
    
    # Verificar si la respuesta fue exitosa
    if response.status_code == 200:
        result = response.json()
        
        # Verificar si hay errores en la respuesta GraphQL
        if "errors" in result:
            print(f"Error GraphQL: {result['errors']}")
        
        return result
    else:
        print(f"Error HTTP: {response.status_code}")
        print(response.text)
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