import json
import re
import datetime
from langchain_core.messages import ToolMessage, AIMessage

from agent.tools.info_pasteleria import info_pasteleria
from agent.tools.get_products import get_products
from agent.tools.get_product import get_product
from agent.tools.get_cocktail import get_cocktail
from agent.tools.get_kutchen import get_kutchen
from agent.tools.get_dessert import get_dessert
from agent.tools.get_products_by_ingredients import get_products_by_ingredients
from agent.tools.get_cakes_by_ingredients import get_cakes_by_ingredients
from agent.tools.get_desserts_by_ingredients import get_desserts_by_ingredients
from agent.tools.get_cocktails_by_ingredients import get_cocktails_by_ingredients
from agent.tools.get_kutchens_by_ingredients import get_kutchens_by_ingredients

tools = [info_pasteleria, get_products, get_product, get_cocktail, get_kutchen, get_dessert, get_products_by_ingredients, get_cakes_by_ingredients, get_desserts_by_ingredients, get_cocktails_by_ingredients, get_kutchens_by_ingredients]
tools_by_name = {tool.__name__: tool for tool in tools}

def execute(message: AIMessage, user_input:str):
    try:
        print("*"*8,"tool","*"*8)
        print(message)
    
        if hasattr(message, "tool_calls") and len(message.tool_calls) > 0:
            tool_calls = message.tool_calls
        elif hasattr(message, "content") and re.search(r'^<function=.+', message.content):
            function_name = re.search(r'function=(\w+)', message.content).group(1)
            match = re.search(r'\{.*\}', message.content)   
            if match:
                json_string = match.group(0)
                try:
                    data = json.loads(json_string)
                except json.JSONDecodeError:
                    raise ValueError("Error: El string extraído no es un JSON válido.")
            else:
                raise ValueError("No se encontró un JSON válido en el string.")
            
            tool_calls = [{'name': function_name, 'args': data, 'id': int(datetime.datetime.now().timestamp())}]
        else:
            outputs = [
                ToolMessage(
                    content=message.content,
                    name="no_function",
                    tool_call_id=int(datetime.datetime.now().timestamp()),
                )
            ]
            return {"messages": outputs}
            # raise ValueError("No function call")

        function_args = ['info_pasteleria','get_products','get_products_by_ingredients','get_cakes_by_ingredients','get_desserts_by_ingredients', 'get_cocktails_by_ingredients','get_kutchens_by_ingredients']
        outputs = []
        for tool_call in tool_calls:
            tool_result = tools_by_name[tool_call["name"]](
                tool_call["args"] if tool_call["name"] in function_args else {'question': user_input}
                # content='{"type": "function", "name": "get_products_by_ingredients", "parameters": {"ingredients": {"type": "array", "items": ["nueces"]}}}
                # tool_calls=[{'name': 'get_products_by_ingredients', 'args': {'ingredients': ['nueces']}, 'id': 'call_78w5', 'type': 'tool_call'}]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}
    except Exception as e:
        raise e