from agent.utils.client_http import client_rag

def get_cocktail(question: str) -> str:
    """function to get product of cocktail from the bakery"""
    print("*"*8,"get_cocktail", "*"*8)
    print(question)
    return client_rag(question['question'])