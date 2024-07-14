# Querying chat models with Together AI

from dotenv import load_dotenv
import os
from tools import ActionGenerator
from prompts import MAIN_AGENT_PROMPT, MESSAGE_TO_AGENT
# Load environment variables from .env file
load_dotenv()
TOGETHER_API_KEY = os.getenv('OPENAI_API_KEY')
# choose from our 50+ models here: https://docs.together.ai/docs/inference-models
from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(
#     base_url="https://api.together.xyz/v1",
#     api_key=TOGETHER_API_KEY,
#     model="mistralai/Mixtral-8x7B-Instruct-v0.1",)
llm = ChatOpenAI(
    api_key=TOGETHER_API_KEY,
    model="gpt-4o",)

#llama does not have function calling :(
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

tools = [ActionGenerator()]

# if you don't want to do streaming, you can use the invoke method
#print(llm.invoke("Tell me fun things to do in NYC").content)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            MAIN_AGENT_PROMPT.format(company_name="LlamaIndex"),
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Construct the Tools agent

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor= AgentExecutor.from_agent_and_tools(
            agent,
            tools,
            return_intermediate_steps=True,
            verbose=True,
            max_iterations=3,
            handle_parsing_errors=True,
        )


# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
# agent_executor.invoke({"input": MESSAGE_TO_AGENT.format(message="I like the way LLamaIndex is deduplicating nodes in KG",
#                                       predicted_tags="appreciation",
#                                       sub_tags=["appreciation","community-building"])},
#                                       return_only_outputs=False,
#                                       include_run_info=True)

x=agent_executor.invoke({"input": MESSAGE_TO_AGENT.format(message="Hey guys, is there any qa_template I can use for my query engine (RAG)? I am writing my own where I would specify that the answer should be concise and contain no meta data / context information, yet the chatbot does not always follow the template for some questions.",
                                      predicted_tags="needs_help",
                                      sub_tags=["needs_help","dev_help"])},
                                      return_only_outputs=False,
                                      include_run_info=True,
                                      )
print(x)
