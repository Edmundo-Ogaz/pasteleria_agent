from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from agent.structure import graph
from agent.utils.State import State

load_dotenv()

app = FastAPI()

@app.get("/agent")
def ejecutar_agente(query: str):
    estado_inicial = State(user_input=query)
    estado_final = graph.invoke(estado_inicial)
    return {"response": estado_final['messages'][-1].content}
