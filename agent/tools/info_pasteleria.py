import requests
import json
import time
import os

# Función para hablar sobre la pastelería
def info_pasteleria(question: str) -> str:
    """function to get info about the bakery for example: history, address, phone"""
    print("*"*8,"info_pasteleria", "*"*8)
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

    retries=3 
    delay=2
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()['respuesta']
        except requests.exceptions.HTTPError as e:
                if response.status_code in [502, 503] and attempt < retries - 1:
                    time.sleep(delay)
                    print(f"retry")
                    continue
                print(f"Fallo permanente: {e}")
                raise
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            return None
        except json.JSONDecodeError:
            print("Response is not valid JSON")
            return response.text #return the text in case of decoding error.

    return ''