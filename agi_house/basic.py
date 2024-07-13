import discord
from discord.ext import commands

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')

@bot.event
async def on_message(message):
    print(f"Received message: {message.content}")  # Debug print
    
    if message.author == bot.user:
        return

    if 'hi' in message.content.lower():
        print("Responding to 'hi'")  # Debug print
        await message.channel.send('hello')
    
    await bot.process_commands(message)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('MTI2MTc3NDU1MzE4OTg0NzA2MQ.GRYbKC.wvk9sBn682tE_mYsCXkGCmJoFPQ65pYKje0gUk')