from fastapi import FastAPI, HTTPException
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

from utils.BasicToolNode import BasicToolNode
from utils.State import State
from utils.route_tools import route_tools
from utils.client_graphql import buscar_productos_por_ingrediente

from tools.info_pasteleria import info_pasteleria
from tools.get_products import get_products
from tools.get_products_by_ingredient import get_products_by_ingredient

from agent.nodes.init import init
from agent.nodes.end import end

load_dotenv()

app = FastAPI()

tools = [info_pasteleria, get_products, get_products_by_ingredient]
llm = ChatGroq( model="llama-3.3-70b-versatile", temperature=0.0, max_retries=2)
llm_with_tools = llm.bind_tools(tools)

# def init(state: State):
#     print("*"*8,"init", "*"*8)
#     print(state)
#     message = llm_with_tools.invoke([{"role": "user", "content": state["user_input"]}])
#     print("*"*8,message, "*"*8)
#     return {"messages": [message]}

# def end(state: State):
#     print("*"*8,"end", "*"*8)
#     print(state)
#     tool_message = state["messages"][-1].content
#     print(tool_message)
#     system_prompt = f"""
#         Eres un asistente amigable de la Pastelería la Palmera. Tu rol es proporcionar información precisa sobre nuestros productos y servicios.

#         Directrices principales:
#         - Responde de forma precisa, concisa y breve
#         - Utiliza EXCLUSIVAMENTE la información del contexto proporcionado
#         - No inferir ni inventar información adicional
#         - No realices suposiciones sobre productos, precios o servicios no mencionados explícitamente
#         - Responde siempre en el mismo idioma de la pregunta
#         - Mantén un tono amable y servicial

#         Contexto:
#         {tool_message}
#     """
#     messages = [
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": state["user_input"]},
#     ]
#     print(messages)
#     message = llm.invoke(messages)
#     print("*"*8,message, "*"*8)
#     # state['response'] = message
#     return {"messages": [message]}

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
