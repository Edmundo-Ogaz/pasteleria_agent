def client_rag(query, url=None, headers=None):
    """
    Sends a POST request to the specified URL with the given data and headers.
    
    Args:
        url (str): The URL to send the POST request to.
        data (dict): The data to include in the POST request.
        headers (dict, optional): Headers to include in the request. Defaults to None.
    
    Returns:
        dict: The JSON response from the server if successful, or an empty string if not.
    """
    import requests
    import json
    import time
    import os

    host = os.environ.get('PASTELERIA_RAG')
    url = f"{host}/ask-model"

    if headers is None:
        headers = {
            "Content-Type": "application/json",
            "sessionId": str(int(time.time())), # Generates a timestamp as a string
        }

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