from fastapi import FastAPI, HTTPException
import langgraph
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langchain.schema import SystemMessage

app = FastAPI()

# Definir el estado del agente
class AgentState:
    def __init__(self, user_input):
        self.user_input = user_input
        self.response = None

llm = ChatGroq( model="llama-3.3-70b-versatile", temperature=0.0, max_retries=2)

# Función para hablar sobre la pastelería
def info_pasteleria(state: AgentState):
    prompt = """
    Eres un asistente de una pastelería llamada "Dulces Delicias".
    Habla sobre la historia de la pastelería, su ubicación y sus especialidades.
    """
    response = llm([SystemMessage(content=prompt)])
    state.response = response.content
    return state

# Función para responder sobre productos
def info_productos(state: AgentState):
    prompt = f"""
    Eres un asistente de una pastelería llamada "Dulces Delicias".
    Responde preguntas sobre los productos como ingredientes, precios y disponibilidad.
    Pregunta del usuario: {state.user_input}
    """
    response = llm([SystemMessage(content=prompt)])
    state.response = response.content
    return state

# Función para clasificar la pregunta del usuario
def clasificar_pregunta(state: AgentState):
    if any(word in state.user_input.lower() for word in ["historia", "ubicación", "especialidad", "quiénes son"]):
        return "pasteleria"
    else:
        return "productos"

# Construcción del gráfico
workflow = StateGraph(AgentState)
workflow.add_node("clasificar", clasificar_pregunta)
workflow.add_node("pasteleria", info_pasteleria)
workflow.add_node("productos", info_productos)

workflow.set_entry_point(clasificar_pregunta)
workflow.add_edge("pasteleria", END)
workflow.add_edge("productos", END)

# Compilar el gráfico
graph = workflow.compile()

# Endpoint para interactuar con el agente
@app.post("/consulta")
def ejecutar_agente(pregunta: str):
    estado_inicial = AgentState(user_input=pregunta)
    estado_final = graph.invoke(estado_inicial)
    return {"respuesta": estado_final.response}
