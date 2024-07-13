import discord
from discord.ext import commands
import json
import aiohttp
import requests
from dotenv import load_dotenv
import os
# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='\\', intents=intents)
# Dictionary to store tags
tags = {}
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('BOT_API_KEY')
API_KEY = os.getenv('ATTUNA_API_KEY')

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
    thread = await ctx.message.create_thread(name=f"Thread for {ctx.message.content}")
    await thread.send(f'Tag added: {response}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    predicted_tags = predict_tags(message.content)
    thread = await message.create_thread(name=f"Thread for {message.content}")
    await thread.send(f'Predicted tags: {predicted_tags}')
    
    await bot.process_commands(message)

# Run the bot
# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('MTI2MTc3NDU1MzE4OTg0NzA2MQ.GRYbKC.wvk9sBn682tE_mYsCXkGCmJoFPQ65pYKje0gUk')