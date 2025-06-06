import requests
import json
import time
import os

with open("./agent/resources/products.json", "r", encoding="utf-8") as archivo:
    products = json.load(archivo)

# Función para hablar sobre la pastelería
def get_cocktail(question: str) -> str:
    """function to get product of cocktail from the bakery"""
    # f"""Obtiene información sobre productos específicos del catálogo. Úsalo cuando el usuario mencione un nombre de producto como {products}."""
    print("*"*8,"get_cocktail", "*"*8)
    print(question)
    # prompt = """
    # Eres un asistente de una pastelería llamada "Dulces Delicias".
    # Habla sobre la historia de la pastelería, su ubicación y sus especialidades.
    # """
    # response = llm([SystemMessage(content=prompt)])
    # state.response = response.content
    # state['response'] = 'info_pasteleria'
    host = os.environ.get('PASTELERIA_RAG')
    url = f"{host}/ask-model"
    headers = {
        "Content-Type": "application/json",
        "sessionId": str(int(time.time())), # Generates a timestamp as a string
    }
    query = question['question']
    data = {"query": query}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()['respuesta']
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None
    except json.JSONDecodeError:
        print("Response is not valid JSON")
        return response.text #return the text in case of decoding error.

    return ''