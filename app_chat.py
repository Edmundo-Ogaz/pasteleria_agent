from fastapi import FastAPI, HTTPException
import langgraph
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langchain.schema import SystemMessage
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages

from typing import Annotated
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
    
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# Función para hablar sobre la pastelería
def info_pasteleria(state: AgentState):
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

# Función para responder sobre productos
# def info_productos(state: AgentState):
#     """function to get the products of the bakery"""
#     print("*"*8,"info_productos", "*"*8)
#     prompt = f"""
#     Eres un asistente de una pastelería llamada "Dulces Delicias".
#     Responde preguntas sobre los productos como ingredientes, precios y disponibilidad.
#     Pregunta del usuario: {state['messages']}
#     """
#     # response = llm([SystemMessage(content=prompt)])
#     # state.response = response.content
#     state['response'] = 'info_productos'
#     return state

def get_products_by_ingredient(ingredient: str) -> str:
    """function to get the products by a ingredient"""
    return f"los productos que tienen {ingredient} son: torta Afrinana y torta Delicias"

# Función para clasificar la pregunta del usuario
# def clasificar_pregunta(state: AgentState):
#     print(state, "-"*8)
#     if any(word in state['user_input'].lower() for word in ["historia", "ubicación", "especialidad", "quiénes son"]):
#         return ["pasteleria"]
#     else:
#         return ["productos"]

tools = [info_pasteleria, get_products_by_ingredient]
llm = ChatGroq( model="llama-3.3-70b-versatile", temperature=0.0, max_retries=2)
llm_with_tools = llm.bind_tools(tools)

def init(state: AgentState):
    print("*"*8,"init", "*"*8)
    print(state)
    message = llm_with_tools.invoke(state["messages"])
    print("*"*8,message, "*"*8)
    if len(message.tool_calls) > 1:
        del message.tool_calls[1]
    return {"messages": [message]}

# Construcción del gráfico
workflow = StateGraph(AgentState)
workflow.add_node("init", init)
workflow.add_node("tools", ToolNode(tools=tools))
# workflow.add_node("pasteleria", info_pasteleria)
# workflow.add_node("productos", info_productos)
workflow.set_entry_point("init")
workflow.add_edge("tools", "init")

workflow.add_conditional_edges(
    "init",
    tools_condition,
)

# workflow.add_edge("pasteleria", END)
# workflow.add_edge("productos", END)

# Compilar el gráfico
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)
# graph = workflow.compile()

# Endpoint para interactuar con el agente
@app.post("/consulta")
def ejecutar_agente(pregunta: str):
    # estado_inicial = AgentState(user_input=pregunta)
    # estado_final = graph.invoke(estado_inicial)
    # estado_final = graph.invoke({"messages": [{"role": "user", "content": pregunta}]})
    events = graph.stream(
        {"messages": [{"role": "user", "content": pregunta}]},
        {"configurable": {"thread_id": "1"}},
        stream_mode="values",
    )
    print("+"*8, "events", "+"*8)
    responses = []
    for event in events:
        event["messages"][-1].pretty_print()
        responses.append(event["messages"][-1].content)

    print("*"*8,"events","*"*8)
    print(list(events))
    # return {"respuesta": "estado_final['response']"}
    return {"respuesta": responses[-1]}
