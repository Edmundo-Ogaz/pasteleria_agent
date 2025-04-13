from langgraph.graph import StateGraph, START, END

from agent.utils.State import State
from agent.utils.BasicToolNode import BasicToolNode
from agent.utils.route_tools import route_tools

from agent.nodes.preprocess import preprocess
from agent.nodes.assign_workers import assign_workers
from agent.nodes.worker import worker
from agent.nodes.end import end

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

workflow = StateGraph(State)
workflow.add_node("preprocess", preprocess)
workflow.add_node("worker", worker)
workflow.add_node("tools", BasicToolNode(tools=tools))
workflow.add_node("end", end)

workflow.add_edge(START, "preprocess")
workflow.add_conditional_edges( "preprocess", assign_workers, ["worker"] )
# workflow.add_conditional_edges( "worker", route_tools, {"tools": "tools", END: END} )
# workflow.add_edge("tools", "end")
workflow.add_edge( "worker", "end" )
workflow.add_edge("end", END)

graph = workflow.compile()