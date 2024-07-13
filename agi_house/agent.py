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
    sub_tags_list = list(sub_tags)
    response = add_tag(sub_tags_list, tag_description, tag_name)
    embed = discord.Embed(title=f"Tag: {tag_name}", description=tag_description, color=discord.Color.blue())
    embed.add_field(name="Sub-tags", value=", ".join(sub_tags_list), inline=False)
    thread = await ctx.message.create_thread(name=f"Thread for {ctx.message.content}")
    await thread.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    predicted_tags = predict_tags(message.content)
    print("Predicted tags: ", predicted_tags)
    embed = discord.Embed(title="Predicted Tags", description="", color=discord.Color.green())
    for tag in predicted_tags["predicted_tags"]:
        tag_name = tag.split(':')[0]
        subtags = tag.split(':')[1]
        embed.add_field(name="Tag", value=tag_name, inline=False)
        embed.add_field(name="Sub-tags", value=subtags, inline=False)
    thread = await message.create_thread(name=f"Thread for {message.content}")
    await thread.send(embed=embed)
    
    await bot.process_commands(message)

# Run the bot
bot.run(DISCORD_BOT_TOKEN)