from agent.utils.client_graphql import graphql_client_basic

def formatear_lista(lista):
    if not lista:
        return ""
    if len(lista) == 1:
        return lista[0]
    return ", ".join(lista[:-1]) + " y " + lista[-1]

def get_kutchens_by_ingredients(ingredients: list) -> str:
    # """function to get the products by a ingredient"""
    """Obtiene las kutchens que contienen estos ingredientes."""
    print("*"*8,"get_kutchens_by_ingredients", "*"*8)
    print(ingredients)

    query = """
    query SearchKutchensByIngredient($ingredients: [String!]!) {
        kutchensByIngredients(ingredientNames: $ingredients) {
            name
        }
    }
    """
    
    # Definir las variables para la consulta
    variables = {
        "ingredients": ingredients['ingredients']
    }
    
    # Realizar la consulta
    result = graphql_client_basic(query, variables)
    
    response = []
    if result and "data" in result and "kutchensByIngredients" in result["data"]:
        response = result["data"]["kutchensByIngredients"]
        
    if response:
        return f"los kutchens que tienen {formatear_lista(ingredients['ingredients'])} son: {response}"
    else:
        return "Para productos especiales, te recomendamos comunicarte directamente con la pastelería al número 55 2 268988 para verificar disponibilidad y opciones."