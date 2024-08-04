from typing import List, TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from prompts import SYSTEM_PROMPT
from config import COMPANY, PROJECT, AGENT_MODEL
from utils import parse_output, fetch_docs
from typing import Any
from langchain_core.pydantic_v1 import BaseModel, Field
# Data model
class CodeGeneration(BaseModel):
    """Code output"""

    prefix: str = Field(description="Description of the problem and approach")
    imports: str = Field(description="Code block import statements")
    code: str = Field(description="Code block not including import statements")
    description = "Schema for code solutions to questions."

class CanDo(BaseModel):
    """Code output"""

    possible: bool = Field(description="Can this use case be performed using the library?")
    reason: str = Field(description="Why or why not?")
    description = "Schema for can the library perform the use case or not responses."

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        error : Binary flag for control flow to indicate whether test error was tripped
        messages : With user question, error messages, reasoning
        generation : Code solution
        iterations : Number of tries
        is_possible : Can the library perform the use case or not
    """
    
    error: str
    messages: List
    generation: str
    iterations: int
    is_possible: bool