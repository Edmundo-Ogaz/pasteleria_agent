from agent.utils.client_http import client_rag

def get_dessert(question: str) -> str:
    """function to get dessert from the bakery"""
    print("*"*8,"get_dessert", "*"*8)
    print(question)
    return client_rag(question['question'])