from langgraph.graph import END, StateGraph, START
from prompts import SYSTEM_PROMPT, CAN_DO_PROMPT
from config import * 
from tools import decide_to_finish, can_answer
from state import GraphState
from nodes import generate, code_check, reflect, answer_can_do
from utils import fetch_docs, parse_output
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from state import CodeGeneration, CanDo
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
    llm_code_gen = ChatOpenAI(temperature=0, model=AGENT_MODEL)
    llm_can_do = ChatOpenAI(temperature=0, model=AGENT_MODEL)
    can_do_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                CAN_DO_PROMPT,
            ),
            ("placeholder", "{messages}"),
        ]
    )

    structured_llm = llm_code_gen.with_structured_output(CodeGeneration, include_raw=True)
    can_do_llm = llm_can_do.with_structured_output(CanDo, include_raw=True)
    return (code_gen_prompt | structured_llm | parse_output, can_do_prompt | can_do_llm | parse_output,docs)


globals.code_gen_chain, globals.can_do_chain, globals.docs = setup() 

workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("can_do", answer_can_do)  # can do
workflow.add_node("generate", generate)  # generation solution
workflow.add_node("check_code", code_check)  # check code
workflow.add_node("reflect", reflect)  # reflect

# Build graph
workflow.add_edge(START, "can_do")
workflow.add_conditional_edges(
    "can_do",
    can_answer,
    {
        "end": END,
        "generate": "generate",
    },
)
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