from langgraph.graph import END
from agent.utils.WorkerState import WorkerState
import re

def route_tools(
    state: WorkerState,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    print("*"*8,"route","*"*8)
    print(state)
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if ((hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0) or
        (hasattr(ai_message, "tool_calls") and re.search(r'^<function=.+</function>', ai_message.content))):
        return "tools"
    return END