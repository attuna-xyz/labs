from typing import Optional, Type

from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from typing import List, Optional
from enum import Enum

class Action(Enum):
    NOTIFY = "NOTIFY"
    RESPOND = "RESPOND"

class DevRelInput(BaseModel):
    tag: str = Field(description="The tag detected in the message")
    sub_tags: List[str] = Field(description="The sub tags detected in the message", default=[])
    message: str = Field(description="The message from the user", default="")

class DevRelOutput(BaseModel):
    action: Action = Field(description="The action to take", default=None)
    message: Optional[str] = Field(description="The message to send", default="")

async def send_message_to_channel(channel_name, message):
    for guild in bot.guilds:
        for channel in guild.channels:
            if channel.name == channel_name and isinstance(channel, discord.TextChannel):
                await channel.send(message)
                return
class ActionGenerator(BaseTool):
    name = "ACTION_GENERATOR"
    description = "Always call this tool at the end to generate an action in appropriate format"
    args_schema: Type[BaseModel] = DevRelOutput
    
    def _run(
        self, action: Action, message: Optional[str], run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """"""
        #save the action and message in a file
        with open('action.txt', 'w') as f:
            f.write(f"{action.value}:::{message}")
        return DevRelOutput(action=action, message=message)

# Querying chat models with Together AI

from dotenv import load_dotenv
import os
#from tools import ActionGenerator
from prompts import MAIN_AGENT_PROMPT, MESSAGE_TO_AGENT
# Load environment variables from .env file
load_dotenv()
# choose from our 50+ models here: https://docs.together.ai/docs/inference-models
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
# llm = ChatOpenAI(
#     base_url="https://api.together.xyz/v1",
#     api_key=TOGETHER_API_KEY,
#     model="mistralai/Mixtral-8x7B-Instruct-v0.1",)
TOGETHER_API_KEY = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(
    api_key=TOGETHER_API_KEY,
    model="gpt-4o",)

#llama does not have function calling :(


tools = [ActionGenerator()]

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

# x=agent_executor.invoke({"input": MESSAGE_TO_AGENT.format(message="Hey guys, is there any qa_template I can use for my query engine (RAG)? I am writing my own where I would specify that the answer should be concise and contain no meta data / context information, yet the chatbot does not always follow the template for some questions.",
#                                       predicted_tags="needs_help",
#                                       sub_tags=["needs_help","dev_help"])},
#                                       return_only_outputs=False,
#                                       include_run_info=True,
#                                       )
#print(x)

import discord
from discord.ext import commands
import json
import aiohttp
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('BOT_API_KEY')
API_KEY = os.getenv('ATTUNA_API_KEY')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix='\\', intents=intents)
# Dictionary to store tags
tags = {}

def add_tag(sub_tags, tag_description, tag_name):
    print("Calling add tag attuna")
    url = 'https://us-central1-prompt-learner-ca90f.cloudfunctions.net/attuna_tagging/add_tag'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': API_KEY
    }
    print("Adding tag with sub_tags: ", sub_tags, " tag_description: ", tag_description, " tag_name: ", tag_name)
    data = {
        "sub_tags": sub_tags,
        "tag_description": tag_description,
        "tag_name": tag_name
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json() if response.status_code == 200 else f"Error: {response.status_code}, {response.text}"

def predict_tags(message):
    if 'add_tag' in message:
        return {"tag_add":"not an inbound message"}
    url = 'https://us-central1-prompt-learner-ca90f.cloudfunctions.net/attuna_tagging/predict_tags'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': API_KEY
    }
    data = {"message": message}
    
    response = requests.post(url, headers=headers, json=data)
    return response.json() if response.status_code == 200 else f"Error: {response.status_code}, {response.text}"

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    if len(bot.guilds) > 0:
        for guild in bot.guilds:
            print(f'- {guild.name} (id: {guild.id})')
    else:
        print('Bot is not in any guilds. Make sure you\'ve invited it to your server.')

@bot.command(name='add_tag')
async def add_tag_command(ctx, tag_name, tag_description, *sub_tags):
    print("Adding tag with sub_tags: ", sub_tags, " tag_description: ", tag_description, " tag_name: ", tag_name)
    sub_tags_list = list(sub_tags)
    response = add_tag(sub_tags_list, tag_description, tag_name)
    await ctx.send(f"Tag '{tag_name}' added successfully!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
        
    predicted_tags = predict_tags(message.content)
    print("Predicted tags: ", predicted_tags)
    embed = discord.Embed(title="Predicted Tags", description="", color=discord.Color.green())
    all_tags=[]
    all_subtags=[]
    if 'predicted_tags' in predicted_tags.keys():
        for tag in predicted_tags["predicted_tags"]:
            tag_name = tag.split(':')[0]
            all_tags.append(tag_name)
            subtags = tag.split(':')[1]
            all_subtags.append(subtags)
            embed.add_field(name="Tag", value=tag_name, inline=False)
            embed.add_field(name="Sub-tags", value=subtags, inline=False)
        thread = await message.create_thread(name=f"Thread for {message.content}")
        await thread.send(embed=embed)
        
        
        agent_executor.invoke({"input": MESSAGE_TO_AGENT.format(message=message.content,
                                        predicted_tags=all_tags,
                                        sub_tags=all_subtags)},
                                        return_only_outputs=False,
                                        include_run_info=True,
                                        )
        #read the action and message from the file
        with open('action.txt', 'r') as f:
            action, msg = f.read().split(':::')
        if action == 'NOTIFY':
            await send_message_to_channel('dev-rel-notify', msg)
        elif action == 'RESPOND':
            await thread.send(msg)
    await bot.process_commands(message)

# Run the bot
bot.run(DISCORD_BOT_TOKEN)

