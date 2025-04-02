from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from agent.utils.State import State
from agent.utils.prompts import init_system_prompt
from agent.tools.info_pasteleria import info_pasteleria
from agent.tools.get_products import get_products
from agent.tools.get_product import get_product
from agent.tools.get_cocktail import get_cocktail
from agent.tools.get_kutchen import get_kutchen
from agent.tools.get_dessert import get_dessert
from agent.tools.get_products_by_ingredients import get_products_by_ingredients
from agent.tools.get_cakes_by_ingredients import get_cakes_by_ingredients
from agent.tools.get_desserts_by_ingredients import get_desserts_by_ingredients

tools = [info_pasteleria, get_products, get_product, get_cocktail, get_kutchen, get_dessert, get_products_by_ingredients, get_cakes_by_ingredients, get_desserts_by_ingredients]
llm = ChatGroq( model="llama-3.3-70b-versatile", temperature=0.0, max_retries=2)
llm_with_tools = llm.bind_tools(tools)

def init(state: State):
    print("*"*8,"init", "*"*8)
    print(state)

    messages = [
        {"role": "system", "content": init_system_prompt},
        {"role": "user", "content": state["user_input"]},
    ]

    try:
        message = llm_with_tools.invoke(messages)
        print("*"*8,message, "*"*8)
        return {"messages": [message]}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"messages": [SystemMessage(content="No se pudo ejecutar la operación")]}