from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from agent.utils.State import State
from agent.tools.info_pasteleria import info_pasteleria
from agent.tools.get_products import get_products
from agent.tools.get_product import get_product
from agent.tools.get_cocktail import get_cocktail
from agent.tools.get_kutchen import get_kutchen
from agent.tools.get_dessert import get_dessert
from agent.tools.get_products_by_ingredients import get_products_by_ingredients
from agent.tools.get_cakes_by_ingredients import get_cakes_by_ingredients
from agent.tools.get_desserts_by_ingredients import get_desserts_by_ingredients
from agent.utils.WorkerState import WorkerState

from agent.utils.executeTool import execute as execute_tool

tools = [info_pasteleria, get_products, get_product, get_cocktail, get_kutchen, get_dessert, get_products_by_ingredients, get_cakes_by_ingredients, get_desserts_by_ingredients]
llm = ChatGroq( model="llama-3.3-70b-versatile", temperature=0.0, max_retries=2)
llm_with_tools = llm.bind_tools(tools)

init_system_prompt = """
Eres un asistente para una pastelería. Debes responder a los mensajes del usuario de la mejor manera posible.

Para responder a los mensajes, sigue estas instrucciones:

1. **Información general**: Si el usuario pregunta sobre ubicación, horarios o contacto, usa la función `info_pasteleria(query: str)`.
2. **Productos disponibles**: Si el usuario pregunta por los productos disponibles o quiere ver el catálogo, usa la función `get_products(query: str)`.
3. **Producto específico**: Si el usuario pregunta por un producto específico, usa la función `get_product(question: str)`.
4. **Coctelería**: Si el usuario pregunta por un producto de coctelería, usa la función `get_cocktail(question: str)`.
5. **Kutchen**: Si el usuario pregunta por un kutchen, usa la función `get_kutchen(question: str)`.
6. **Postre**: Si el usuario pregunta por un postre, usa la función `get_desert(question: str)`.
7. **Productos por ingrediente**: Si el usuario pregunta por productos con un ingrediente específico, usa la función `get_products_by_ingredients(ingredients: list)`.
8. **Tortas por ingrediente**: Si el usuario pregunta por tortas con un ingrediente específico, usa la función `get_cakes_by_ingredients(ingredients: list)`.
9. **Postres por ingrediente**: Si el usuario pregunta por postres con un ingrediente específico, usa la función `get_desserts_by_ingredients(ingredients: list)`.
10. **Productos especiales**: Si el usuario pregunta por productos sin azúcar, sin gluten, veganos, vegetarianos, sin lactosa, sin huevos u otra variante especial, responde: "Para productos especiales, te recomendamos comunicarte directamente con la pastelería al número 55 2 268988 para verificar disponibilidad y opciones.".
11. **Respuestas simples**: Si el mensaje es simple y puedes responder sin llamar una función (como 'Hola buenos días' o '¿Cómo estás?'), responde directamente.
12. **Respuestas generales**: Si no estás seguro de cómo responder, da una respuesta general y ofrece más ayuda.

Recuerda que, en general, debes pasar el mensaje del usuario tal como está a las funciones correspondientes, a menos que se trate de una consulta por ingrediente, en cuyo caso debes adaptar el mensaje para obtener el ingrediente específico.
"""

def worker(state: WorkerState):
    """Worker analyze the section of the message"""

    print("*"*8,"worker","*"*8)
    print(state)
    messages = [
        {"role": "system", "content": init_system_prompt},
        {"role": "user", "content": state["section"]},
    ]

    message = llm_with_tools.invoke(messages)

    tool_response = execute_tool(message, state["section"])
    return {"messages": [message, tool_response.get("messages")[-1]]}