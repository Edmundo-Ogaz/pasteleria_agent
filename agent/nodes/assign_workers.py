from agent.utils.State import State
from langgraph.constants import Send

def assign_workers(state: State):
    """Assign a worker to each section of the message"""

    # Kick off section writing in parallel via Send() API
    print("*"*8,"assign_workers","*"*8)
    print(state)
    return [Send("worker", {"section": s}) for s in state["sections"]]