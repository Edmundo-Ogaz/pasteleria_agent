from langchain_groq import ChatGroq
from utils.State import State

from tools.info_pasteleria import info_pasteleria
from tools.get_products import get_products
from tools.get_products_by_ingredient import get_products_by_ingredient

tools = [info_pasteleria, get_products, get_products_by_ingredient]
llm = ChatGroq( model="llama-3.3-70b-versatile", temperature=0.0, max_retries=2)
llm_with_tools = llm.bind_tools(tools)

def init(state: State):
    print("*"*8,"init", "*"*8)
    print(state)
    message = llm_with_tools.invoke([{"role": "user", "content": state["user_input"]}])
    print("*"*8,message, "*"*8)
    return {"messages": [message]}