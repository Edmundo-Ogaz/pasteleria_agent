from agent.utils.client_http import client_rag 

def get_product(question: str) -> str:
    """function to get product from the bakery"""
    print("*"*8,"get_product", "*"*8)
    print(question)
    return client_rag(question['question'])