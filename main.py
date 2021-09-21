import os

import discord
from command import on_command, COMMANDS
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("DISCORD_PREFIX")

client = discord.Client()

@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"สวัสดีครับ {member.name} ยินดีต้อนรับ"
        )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if PREFIX == message.content[0:len(PREFIX)]:
        print(f"The bot is called at channel {message.channel.id}")
        words = message.content[1:].split(" ")
        mentions = message.mentions
        for _ in COMMANDS:
            if words[0] not in COMMANDS:
                return 
        await on_command(words, message, mentions, client)

client.run(TOKEN)