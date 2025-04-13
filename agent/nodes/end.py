from agent.utils.State import State
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, ToolMessage

llm = ChatGroq( model="llama-3.3-70b-versatile", temperature=0.0, max_retries=2)

def end(state: State):
    print("*"*8,"end", "*"*8)
    print(state)
    # tool_message = state["messages"][-1].content
    tool_messages = []
    for message in state["messages"]:
        if isinstance(message, ToolMessage):
            tool_messages.append(message.content)
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
        {"/n".join(tool_messages)}
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": state["user_input"]},
    ]
    try:
        message = llm.invoke(messages)
        print("*"*8,message, "*"*8)
        return {"messages": [message]}
    except Exception:
        return {"messages": [SystemMessage(content="No se pudo ejecutar la operación")]}