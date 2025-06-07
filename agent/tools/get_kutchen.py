from agent.utils.client_http import client_rag

def get_kutchen(question: str) -> str:
    """function to get product of kutchen from the bakery"""
    print("*"*8,"get_kutchen", "*"*8)
    print(question)
    return client_rag(question['question'])