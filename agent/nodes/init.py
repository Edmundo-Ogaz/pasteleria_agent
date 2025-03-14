from langchain_groq import ChatGroq
from agent.utils.State import State
from agent.utils.prompts import init_system_prompt
from agent.tools.info_pasteleria import info_pasteleria
from agent.tools.get_products import get_products
from agent.tools.get_product import get_product
from agent.tools.get_products_by_ingredient import get_products_by_ingredient

tools = [info_pasteleria, get_products, get_product, get_products_by_ingredient]
llm = ChatGroq( model="llama-3.3-70b-versatile", temperature=0.0, max_retries=2)
llm_with_tools = llm.bind_tools(tools)

def init(state: State):
    print("*"*8,"init", "*"*8)
    print(state)

    system_prompt = [
        "Eres un asistente para una pastelería. Debes responder a los mensajes del usuario de la mejor manera posible.",
        "",
        "Usa la función info_pasteleria si el usuario pregunta sobre ubicación, horarios o contacto.",
        "Usa la función get_products si el usuario pregunta por los productos disponibles o quiere ver el catálogo y no cambies la pregunta, ingresala a la función como está",
        "Usa la función get_product si el usuario pregunta por un producto espedifico, y no cambies la pregunta, ingresala a la función como está",
        "Usa la función get_products_by_ingredient si el usuario pregunta por productos con un ingrediente específico.",
        "Si el mensaje es simple y puedes responder sin llamar una función (como 'Hola buenos días' o '¿Cómo estás?'), responde directamente.",
        "Si no estás seguro, da una respuesta general y ofrece más ayuda."
    ]
    messages = [
        {"role": "system", "content": init_system_prompt},
        {"role": "user", "content": state["user_input"]},
    ]

    message = llm_with_tools.invoke(messages)
    print("*"*8,message, "*"*8)
    return {"messages": [message]}