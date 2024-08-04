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



class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        error : Binary flag for control flow to indicate whether test error was tripped
        messages : With user question, error messages, reasoning
        generation : Code solution
        iterations : Number of tries
    """
    
    error: str
    messages: List
    generation: str
    iterations: int