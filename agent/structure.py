from langgraph.graph import StateGraph, END

from utils.State import State
from utils.BasicToolNode import BasicToolNode
from utils.route_tools import route_tools

from agent.nodes.init import init
from agent.nodes.end import end

from tools.info_pasteleria import info_pasteleria
from tools.get_products import get_products
from tools.get_products_by_ingredient import get_products_by_ingredient

tools = [info_pasteleria, get_products, get_products_by_ingredient]

workflow = StateGraph(State)
workflow.add_node("init", init)
tool_node = BasicToolNode(tools=tools)
workflow.add_node("tools", tool_node)
workflow.add_node("end", end)

workflow.set_entry_point("init")
workflow.add_conditional_edges(
    "init",
    route_tools,
    {"tools": "tools", END: END},
)
workflow.add_edge("tools", 'end')

graph = workflow.compile()