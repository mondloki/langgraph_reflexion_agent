import json
from typing import List
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage, ToolMessage
from schemas import AnswerQuestion, ReviseAnswer
from chains import parser
# from langgraph.prebuilt import ToolInvocation , ToolExecutor

from langchain_core.tools import StructuredTool
from langgraph.prebuilt import ToolNode

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from collections import defaultdict

search = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search, max_results=5)
# tool_executor = ToolExecutor(tools=[tavily_tool])

# def execute_tools(state: List[BaseMessage]) -> List[ToolMessage]:
#     tool_invocation: AIMessage = state[-1]  
#     parsed_tool_calls = parser.invoke(tool_invocation)


#     ids = []
#     tool_invocations = []

#     for parsed_tool_call in parsed_tool_calls:
#         for query in parsed_tool_call["args"]["search_queries"]:
#             tool_invocations.append(
#                 ToolInvocation(
#                     tool="tavily_search_results_json",
#                     tool_input=query
#                 )
#             )
#             ids.append(parsed_tool_call["id"])
#     outputs = tool_executor.batch(tool_invocations)
#     outputs_map = defaultdict(dict)

#     for id, output, tool_invocation in zip(ids, outputs, tool_invocations):
#         outputs_map[id][tool_invocation.tool_input] = output

#     tool_messages = []

#     for id_, mapped_output in outputs_map.items():
#         tool_messages.append(ToolMessage(content=json.dumps(mapped_output), tool_call_id=id_))
#     return tool_messages

def run_queries(search_queries: list[str], **kwargs):
    """Run the generated queries."""
    return tavily_tool.batch([{"query": query} for query in search_queries])


tool_node = ToolNode(
    [
        StructuredTool.from_function(run_queries, name=AnswerQuestion.__name__),
        StructuredTool.from_function(run_queries, name=ReviseAnswer.__name__),
    ]
)

if __name__ == "__main__":
    
    human_message = HumanMessage(
        content="Write about AI-Powered SOC/ autonomous soc problem domain,"
        "list startups that do that and raised capital"
    )

    answer = AnswerQuestion(
        answer="",
        reflection="",
    search_queries = [
        "AI-powered SOC startups funding Crunchbase",
        "Autonomous SOC investment PitchBook", 
        " Cybersecurity AI startups funding rounds"
    ],
    id= "abf40b50-aaf8-4b60-8a70-95915ec777f9"

    )

    raw_res = execute_tools(
        state=[
            human_message,
            AIMessage(
                content="This is content",
                tool_calls= [
                    {
                        "name": AnswerQuestion.__name__,
                        "args": answer.dict(),
                        "id": "abf40b50-aaf8-4b60-8a70-95915ec777f9"
                    }
                ]
            )
        ]
    )

    print(raw_res)