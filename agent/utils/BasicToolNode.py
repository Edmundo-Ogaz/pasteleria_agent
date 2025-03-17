import json
import re
import datetime
from langchain_core.messages import ToolMessage


class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.__name__: tool for tool in tools}

    def __call__(self, inputs: dict):
        user_input = inputs.get("user_input", "")
        print("user_input", user_input)
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        
        if hasattr(message, "tool_calls") and len(message.tool_calls) > 0:
            tool_calls = message.tool_calls
        elif hasattr(message, "content") and re.search(r'^<function=.+</function>', message.content):
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
 
        outputs = []
        for tool_call in tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]](
                tool_call["args"] if tool_call["name"] == 'get_products_by_ingredient' else {'question': user_input}
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}