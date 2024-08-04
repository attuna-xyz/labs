from config import *
from state import GraphState
from typing import Any
import globals
def generate(state: GraphState):
    """
    Generate a code solution

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation
    """

    print("---GENERATING CODE SOLUTION---")

    # State
    messages = state["messages"]
    iterations = state["iterations"]
    error = state["error"]

    # We have been routed back to generation with an error
    if error == "yes":
        messages += [
            (
                "user",
                "Now, try again. Invoke the code tool to structure the output with a prefix, imports, and code block:",
            )
        ]

    # Solution
    code_solution = globals.code_gen_chain.invoke(
        {"docs": globals.docs, "company": COMPANY ,"project": PROJECT, "messages": messages}
    )
    messages += [
        (
            "assistant",
            f"{code_solution.prefix} \n Imports: {code_solution.imports} \n Code: {code_solution.code}",
        )
    ]
    if iterations is None:
        iterations = 1
    else:
        iterations += 1
    return {"generation": code_solution, "messages": messages, "iterations": iterations}

def code_check(state: GraphState):
    """
    Check code

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, error
    """

    print("---CHECKING CODE---")

    # State
    messages = state["messages"]
    code_solution = state["generation"]
    iterations = state["iterations"]

    # Get solution components
    imports = code_solution.imports
    code = code_solution.code

    # Check imports
    try:
        exec(imports)
    except Exception as e:
        print("---CODE IMPORT CHECK: FAILED---")
        error_message = [("user", f"Your solution failed the import test: {e}")]
        messages += error_message
        return {
            "generation": code_solution,
            "messages": messages,
            "iterations": iterations,
            "error": "yes",
        }

    # Check execution
    try:
        exec(imports + "\n" + code)
    except Exception as e:
        print("---CODE BLOCK CHECK: FAILED---")
        error_message = [("user", f"Your solution failed the code execution test: {e}")]
        messages += error_message
        return {
            "generation": code_solution,
            "messages": messages,
            "iterations": iterations,
            "error": "yes",
        }

    # No errors
    print("---NO CODE TEST FAILURES---")
    return {
        "generation": code_solution,
        "messages": messages,
        "iterations": iterations,
        "error": "no",
    }

def reflect(state: GraphState):
    """
    Reflect on errors

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation
    """

    print("---GENERATING CODE SOLUTION---")

    # State
    messages = state["messages"]
    iterations = state["iterations"]
    code_solution = state["generation"]

    # Prompt reflection

    # Add reflection
    reflections = globals.code_gen_chain.invoke(
        {"docs": globals.docs, "company": COMPANY ,"project": PROJECT, "messages": messages}
    )
    messages += [("assistant", f"Here are reflections on the error: {reflections}")]
    return {"generation": code_solution, "messages": messages, "iterations": iterations}

def answer_can_do(state: GraphState):
    """
    Answer can do

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, can_do
    """

    print("---ANSWERING CAN DO QUESTIONS---")

    # State
    messages = state["messages"]
    is_possible = state["is_possible"]
    if is_possible is True:
        messages += [("user", "Yes, the library can do that! Call the code generation tool to generate a solution.")]
        return {"is_possible": is_possible, "messages": messages}
    elif is_possible is False:
        messages += [("user", "No, the library cannot do that. End the chain")]
        return {"is_possible": is_possible, "messages": messages}
    else:
        # Solution
        can_do = globals.can_do_chain.invoke(
            {"docs": globals.docs, "company": COMPANY ,"project": PROJECT, "messages": messages}
        )
        messages += [
            (
                "assistant",
                f"Can do: {can_do.possible} \n Reason: {can_do.reason}",
            )
        ]
        return {"is_possible": can_do.possible, "messages": messages}