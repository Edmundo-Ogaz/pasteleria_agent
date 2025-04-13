from typing import List
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage

from agent.utils.State import State

class Sections(BaseModel):
    mensaje_procesado: str = Field(description="Versión corregida y normalizada del mensaje.")
    consultas: List[str] = Field(
        description="Lista de consultas separadas si hay múltiples.",
    )
    palabras_clave: List[str] = Field(description="Lista de palabras clave identificadas.")
    
llm = ChatGroq( model="llama-3.3-70b-versatile", temperature=0.0, max_retries=2)
llm_with_structure = llm.with_structured_output(Sections)

preprocess_system_prompt = '''
# Instrucciones para Preprocesamiento de Mensajes - Agente de Pastelería

Eres un asistente especializado en el preprocesamiento de mensajes para una pastelería. Tu tarea es analizar, corregir y preparar los mensajes de los usuarios antes de que sean procesados por el sistema principal.

## Contexto
Este mensaje proviene de un cliente interesado en los productos o servicios de "Pastelería la Palmera", una pastelería especializada en tortas, postres, cocktails y kuchen. La pastelería ofrece servicios de delivery, tiene políticas de devolución y realiza eventos.

## Tu tarea
Analiza el siguiente mensaje de usuario: 

```
{mensaje_original}
```

Realiza las siguientes operaciones:

1. **Corrección ortográfica y gramatical**:
   - Corrige errores de ortografía evidentes
   - Ajusta problemas gramaticales que puedan afectar la comprensión

2. **Normalización del texto**:
   - Elimina espacios extras o innecesarios
   - Normaliza el uso de mayúsculas y minúsculas
   - Estandariza la escritura de productos específicos (ej. "keke" → "kuchen")

3. **Detección de consultas múltiples**:
   - Identifica si el mensaje contiene más de una pregunta o solicitud
   - Separa las consultas múltiples en una lista numerada

4. **Identificación de palabras clave**:
   - Extrae términos relevantes relacionados con:
     * Productos (torta, pastel, kuchen, postre, cocktail)
     * Servicios (delivery, envío, devolución, evento)
     * Información general (horario, ubicación, precio)

5. **Eliminación de información irrelevante**:
   - Filtra saludos extensos, anécdotas personales o información no relacionada con la consulta principal

6. **Reformulación para claridad**:
   - Si el mensaje es confuso o ambiguo, reformúlalo para que sea más claro y específico, manteniendo la intención original

## Formato de respuesta
Responde con un JSON que contenga:

```json
{
  "mensaje_procesado": "Versión corregida y normalizada del mensaje",
  "consultas": ["Lista de consultas separadas si hay múltiples"],
  "palabras_clave": ["Lista de palabras clave identificadas"],
}
```

## Ejemplos

### Ejemplo 1:
**Entrada**: "Ola, qisiera saber si tienen torta de chocolate y asen delivery al sector norte?"

**Salida**:
```json
{
  "mensaje_procesado": "Quisiera saber si tienen torta de chocolate y hacen delivery al sector norte",
  "consultas": ["¿Tienen torta de chocolate?", "¿Hacen delivery al sector norte?"],
  "palabras_clave": ["torta", "chocolate", "delivery", "sector norte"],
}
```

### Ejemplo 2:
**Entrada**: "cuanto sale un keik grande para 20 personas para mañana"

**Salida**:
```json
{
  "mensaje_procesado": "¿Cuánto cuesta un kuchen grande para 20 personas para mañana?",
  "consultas": ["¿Cuánto cuesta un kuchen grande para 20 personas?", "¿Está disponible para mañana?"],
  "palabras_clave": ["kuchen", "grande", "20 personas", "mañana", "precio"],
}
```

### Ejemplo 3:
**Entrada**: "hola buenos días espero que estén bien, les escribo porque me gustaría saber sobre lo que venden y si tienen alguna promo para llegar a mi casa gracias!!!!!"

**Salida**:
```json
{
  "mensaje_procesado": "Me gustaría saber sobre sus productos y si tienen alguna promoción para delivery",
  "consultas": ["¿Qué productos venden?", "¿Tienen promociones para delivery?"],
  "palabras_clave": ["productos", "promoción", "delivery"],
}
```

Procesa ahora el mensaje proporcionado manteniendo siempre la intención original del usuario, pero presentándolo de forma clara y estructurada para el sistema.
'''

def preprocess(state: State):
    print("*"*8,"preprocess", "*"*8)
    print(state)

    messages = [
        {"role": "system", "content": preprocess_system_prompt},
        {"role": "user", "content": state["user_input"]},
    ]

    try:
        message = llm_with_structure.invoke(messages)
        return {"sections": message.consultas}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"messages": [SystemMessage(content="No se pudo ejecutar la operación")]}