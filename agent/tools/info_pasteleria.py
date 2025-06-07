from agent.utils.client_http import client_rag 

def info_pasteleria(question: str) -> str:
    """function to get info about the bakery for example: history, address, phone"""
    print("*"*8,"info_pasteleria", "*"*8)
    print(question)
    return client_rag(question['question'])

