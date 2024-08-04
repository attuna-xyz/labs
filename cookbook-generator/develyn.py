from langgraph.graph import END, StateGraph, START
from prompts import SYSTEM_PROMPT
from config import * 
from tools import decide_to_finish
from state import GraphState
from nodes import generate, code_check, reflect
from utils import fetch_docs, parse_output
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from state import CodeGeneration
import globals

def setup():
    docs = fetch_docs()
    code_gen_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_PROMPT,
            ),
            ("placeholder", "{messages}"),
        ]
    )
    llm = ChatOpenAI(temperature=0, model=AGENT_MODEL)
    structured_llm = llm.with_structured_output(CodeGeneration, include_raw=True)
    return (code_gen_prompt | structured_llm | parse_output, docs)


globals.code_gen_chain, globals.docs = setup() 


workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("generate", generate)  # generation solution
workflow.add_node("check_code", code_check)  # check code
workflow.add_node("reflect", reflect)  # reflect

# Build graph
workflow.add_edge(START, "generate")
workflow.add_edge("generate", "check_code")
workflow.add_conditional_edges(
    "check_code",
    decide_to_finish,
    {
        "end": END,
        "reflect": "reflect",
        "generate": "generate",
    },
)
workflow.add_edge("reflect", "generate")
app = workflow.compile()

#question = "How can I directly pass a string to a runnable and use it to construct the input needed for my prompt?"
#[("user",How can I directly pass a string to a runnable and use it to construct the input needed for my prompt?)]
#app.invoke({"messages": [("user", question)], "iterations": 0})