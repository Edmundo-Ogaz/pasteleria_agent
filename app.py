from fastapi import FastAPI, HTTPException
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from typing import List, Dict
from typing_extensions import TypedDict
from dotenv import load_dotenv

from utils.BasicToolNode import BasicToolNode
from typing import Annotated
from langgraph.graph.message import add_messages
from utils.State import State
from utils.route_tools import route_tools
from utils.client_graphql import buscar_productos_por_ingrediente

from tools.info_pasteleria import info_pasteleria

load_dotenv()

app = FastAPI()

# Función para hablar sobre la pastelería
# def info_pasteleria(state: State):
#     """function to get info about the bakery for example: history, address, phone"""
#     print("*"*8,"info_pasteleria", "*"*8)
#     prompt = """
#     Eres un asistente de una pastelería llamada "Dulces Delicias".
#     Habla sobre la historia de la pastelería, su ubicación y sus especialidades.
#     """
#     # response = llm([SystemMessage(content=prompt)])
#     # state.response = response.content
#     state['response'] = 'info_pasteleria'
#     return state

def get_products_by_ingredient(ingredient: str) -> str:
    """function to get the products by a ingredient"""
    print("*"*8,"get_products_by_ingredient", "*"*8)
    print("-"*8, ingredient, "-"*8)
    parameter = ingredient['ingredient']
    products = buscar_productos_por_ingrediente(parameter)
    # ingredient = state['model'].tool_calls[0]['args']['ingredient']
    # return f"los productos que tienen {ingredient} son: torta Afrinana y torta Delicias"
    # state['response'] = f'los productos que tienen {ingredient} son: torta Afrinana y torta Delicias'
    # return f'los productos que tienen {ingredient} son: torta Afrinana y torta Delicias'
    return f'los productos que tienen {parameter} son: {products}'

tools = [info_pasteleria, get_products_by_ingredient]
llm = ChatGroq( model="llama-3.3-70b-versatile", temperature=0.0, max_retries=2)
llm_with_tools = llm.bind_tools(tools)

def init(state: State):
    print("*"*8,"init", "*"*8)
    print(state)
    message = llm_with_tools.invoke([{"role": "user", "content": state["user_input"]}])
    print("*"*8,message, "*"*8)
    return {"messages": [message]}

def end(state: State):
    print("*"*8,"end", "*"*8)
    print(state)
    tool_message = state["messages"][-1].content
    print(tool_message)
    system_prompt = f"""
        Eres un asistente amigable de la Pastelería la Palmera. Tu rol es proporcionar información precisa sobre nuestros productos y servicios.

        Directrices principales:
        - Responde de forma precisa, concisa y breve
        - Utiliza EXCLUSIVAMENTE la información del contexto proporcionado
        - No inferir ni inventar información adicional
        - No realices suposiciones sobre productos, precios o servicios no mencionados explícitamente
        - Responde siempre en el mismo idioma de la pregunta
        - Mantén un tono amable y servicial

        Contexto:
        {tool_message}
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": state["user_input"]},
    ]
    print(messages)
    message = llm.invoke(messages)
    print("*"*8,message, "*"*8)
    # state['response'] = message
    return {"messages": [message]}

workflow = StateGraph(State)
workflow.add_node("init", init)
tool_node = BasicToolNode(tools=tools)
workflow.add_node("tools", tool_node)
workflow.add_node("end", end)

workflow.set_entry_point("init")
workflow.add_conditional_edges(
    "init",
    route_tools,
    {"tools": "tools", END: END},
)
workflow.add_edge("tools", 'end')

graph = workflow.compile()

@app.get("/agent")
def ejecutar_agente(query: str):
    estado_inicial = State(user_input=query)
    estado_final = graph.invoke(estado_inicial)
    return {"response": estado_final['messages'][-1].content}
