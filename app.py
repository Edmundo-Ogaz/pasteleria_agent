from fastapi import FastAPI, HTTPException
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from typing import List, Dict
from typing_extensions import TypedDict
from dotenv import load_dotenv

from BasicToolNode import BasicToolNode
from typing import Annotated
from langgraph.graph.message import add_messages

load_dotenv()

app = FastAPI()

# class ToolCall(TypedDict):
#     name: str
#     args: Dict[str, str]
    
# class Model(TypedDict):
#     content: str
#     tool_calls: List[ToolCall]
    
class State(TypedDict):
    user_input: str
    messages: Annotated[list, add_messages]

def route_tools(
    state: State,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END

# Función para hablar sobre la pastelería
def info_pasteleria(state: State):
    """function to get info about the bakery for example: history, address, phone"""
    print("*"*8,"info_pasteleria", "*"*8)
    prompt = """
    Eres un asistente de una pastelería llamada "Dulces Delicias".
    Habla sobre la historia de la pastelería, su ubicación y sus especialidades.
    """
    # response = llm([SystemMessage(content=prompt)])
    # state.response = response.content
    state['response'] = 'info_pasteleria'
    return state

def get_products_by_ingredient(ingredient: str) -> str:
    """function to get the products by a ingredient"""
    print("*"*8,"get_products_by_ingredient", "*"*8)
    print("-"*8, ingredient, "-"*8)
    # ingredient = state['model'].tool_calls[0]['args']['ingredient']
    # return f"los productos que tienen {ingredient} son: torta Afrinana y torta Delicias"
    # state['response'] = f'los productos que tienen {ingredient} son: torta Afrinana y torta Delicias'
    return f'los productos que tienen {ingredient} son: torta Afrinana y torta Delicias'

# def clasification(state: State):
#     print("*"*8,"clasification", "*"*8)
#     print("-"*8, state, "-"*8)
#     if state['model'].content:
#         state['response'] = state['model'].content
#         return ['end']
#     elif state['model'].tool_calls:
#         return state['model'].tool_calls[0]['name']
#     else:
#         return ['info_pasteleria']

tools = [info_pasteleria, get_products_by_ingredient]
llm = ChatGroq( model="llama-3.3-70b-versatile", temperature=0.0, max_retries=2)
llm_with_tools = llm.bind_tools(tools)

def init(state: State):
    print("*"*8,"init", "*"*8)
    print(state)
    message = llm_with_tools.invoke([{"role": "user", "content": state["user_input"]}])
    print("*"*8,message, "*"*8)
    # state['messages'] = message
    return {"messages": [message]}

# def end(state: State):
#     print("*"*8,"end", "*"*8)
#     print(state)
#     message = llm.invoke([{"role": "user", "content": state["user_input"]}, {"role": "ai", "content": state["response"]}])
#     print("*"*8,message, "*"*8)
#     state['response'] = message
#     return state

workflow = StateGraph(State)
workflow.add_node("init", init)
# workflow.add_node("info_pasteleria", info_pasteleria)
# workflow.add_node("get_products_by_ingredient", get_products_by_ingredient)
tool_node = BasicToolNode(tools=tools)
workflow.add_node("tools", tool_node)
# workflow.add_node("end", end)

workflow.set_entry_point("init")
# workflow.add_conditional_edges( "init", clasification)
workflow.add_conditional_edges(
    "init",
    route_tools,
    {"tools": "tools", END: END},
)
# workflow.add_edge("info_pasteleria", "end")
# workflow.add_edge("get_products_by_ingredient", "end")
# workflow.add_edge("end", END)

graph = workflow.compile()

@app.post("/consulta")
def ejecutar_agente(pregunta: str):
    estado_inicial = State(user_input=pregunta)
    estado_final = graph.invoke(estado_inicial)
    return {"respuesta": estado_final}
