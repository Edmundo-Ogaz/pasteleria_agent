from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
import operator

class State(TypedDict):
    user_input: str
    sections: list[str]
    # messages: Annotated[list, add_messages]
    messages: Annotated[list, operator.add]