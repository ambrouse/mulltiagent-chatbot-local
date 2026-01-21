from typing import TypedDict, List, Optional
from agent_chatbot.agent_state.agent_state import ContractState
from backend.agent_chatbot.node.contract_create_node import analysis_value_input_node, ask_value_input_node, ask_or_create_node, create_word
from langgraph.graph import StateGraph, END


workflow = StateGraph(ContractState)
workflow.add_node("contract_create_node", analysis_value_input_node)
workflow.add_node("ask_value_input_node", ask_value_input_node)
# workflow.add_node("ask_or_create_node", ask_or_create_node)
workflow.add_node("create_word", create_word)


workflow.set_entry_point("contract_create_node")
# workflow.add_edge("contract_create_node", "ask_value_input_node")
workflow.add_conditional_edges(
    "contract_create_node",
    ask_or_create_node,
    {
        "create_word":"create_word",
        "ask_value_input_node":"ask_value_input_node"                        
    }

)


workflow.add_edge("create_word", END)
workflow.add_edge("ask_value_input_node", END)

app_workflow = workflow.compile()