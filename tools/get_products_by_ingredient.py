from utils.client_graphql import graphql_client_basic

def get_products_by_ingredient(ingredient: str) -> str:
    """function to get the products by a ingredient"""
    print("*"*8,"get_products_by_ingredient", "*"*8)
    print("-"*8, ingredient, "-"*8)

    query = """
    query SearchProductsByIngredient($ingredient: String!) {
        productsByIngredient(ingredientName: $ingredient) {
            name
        }
    }
    """
    
    # Definir las variables para la consulta
    variables = {
        "ingredient": ingredient['ingredient']
    }
    
    # Realizar la consulta
    result = graphql_client_basic(query, variables)
    
    response = []
    if result and "data" in result and "productsByIngredient" in result["data"]:
        response = result["data"]["productsByIngredient"]
        
    return f"los productos que tienen {ingredient['ingredient']} son: {response}"