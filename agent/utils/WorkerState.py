from typing_extensions import TypedDict
from typing import Annotated
import operator

class WorkerState(TypedDict):
    section: str
    messages: Annotated[list, operator.add]