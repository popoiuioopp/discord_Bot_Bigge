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

@client.event
async def on_voice_state_update(member, before, after):
    channel = member.guild.text_channels[4]
    if before.channel != after.channel:
        text = f"{member.mention} "
        text = text + f"leaved {before.channel.mention} " if before.channel else text
        text = text + f"and " if before.channel and after.channel else text
        text = text + f"joined {after.channel.mention} " if after.channel else text
        await channel.send(text)
    else:
        if after.self_mute:
            await channel.send(f"{member.mention} ปิดไมค์")
        if after.self_deaf:
            await channel.send(f"{member.mention} ปิดเสียง")

client.run(TOKEN) 