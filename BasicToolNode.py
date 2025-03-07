import json

from langchain_core.messages import ToolMessage


class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.__name__: tool for tool in tools}
        # self.tools_by_name = {tool: tool for tool in tools}

    def __call__(self, inputs: dict):
        print("*"*8, inputs, "*"*8)
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            print(self.tools_by_name)
            # tool_result = self.tools_by_name[tool_call["name"]].invoke(
            #     tool_call["args"]
            # )
            tool_result = self.tools_by_name[tool_call["name"]](
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}