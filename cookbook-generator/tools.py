from config import MAX_RETRIES


from state import GraphState
from typing import Any



def decide_to_finish(state: GraphState):
    """
    Determines whether to finish.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    error = state["error"]
    iterations = state["iterations"]

    if error == "no" or iterations == MAX_RETRIES:
        print("---DECISION: FINISH---")
        return "end"
    else:
            return "generate"
        
def can_answer(state: GraphState):
    """
    Determines whether to finish.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    is_possible = state["is_possible"]
    if is_possible is True:
        print("---DECISION: CAN DO---")
        return "generate"
    elif is_possible is False:
        print("---DECISION: CAN NOT DO---")
        return "end"
    else:
        return "end"