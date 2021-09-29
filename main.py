import os, asyncio, datetime, json
import discord
from discord.ext import commands
from dotenv import load_dotenv
from gtts import gTTS
from collections import deque
from tempfile import TemporaryFile

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("DISCORD_PREFIX")

tts_focusing = {}

bot = commands.Bot(command_prefix=PREFIX, description="WowZa bot V0.2")

async def getTTS(message):
    tts = gTTS(message, lang='th')
    f = TemporaryFile()
    tts.write_to_fp(f)
    f.seek(0)
    return f

@bot.event
async def on_ready():
    print("WowZa is ready to serve!")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Hello World!", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")

    await ctx.send(embed=embed)

@bot.command()
async def clear(ctx):
    botQuestionMessage = await ctx.message.channel.send("Are you sure you want to clear the messages? type \"Yes or No\"")
    clearingMessage = "👍 Clearing "

    def check(m):
        return (m.content == "Yes" or m.content == "No") and m.channel == ctx.message.channel and m.author == ctx.message.author
    msg=None
    try:
        msg = await ctx.bot.wait_for('message', check=check, timeout=6)
    except asyncio.TimeoutError:
        await ctx.message.channel.send('👎 Timed out')

    if msg.content != "Yes":
        botRecentMessage = await ctx.message.channel.send("Okay, I won't clear the messages.")
        await asyncio.sleep(5)
        await msg.delete(delay=3)
        await botQuestionMessage.delete(delay=3)
        await botRecentMessage.delete(delay=3)
        return
    if ctx.message.mentions:
        if not ctx.message.author.guild_permissions.administrator and ctx.message.mentions[0] != ctx.message.author: 
            await ctx.message.channel.send("You don't have permission to clear messages")
            return
    
        if ctx.message.author == ctx.message.author:
            clearingMessage += "all your messages"

    clearingMessage += ".."
    botRecentMessage = await ctx.message.channel.send(clearingMessage)
    async for m in ctx.message.channel.history(limit=100):
        if m == botRecentMessage:
            continue
        if not ctx.message.mentions or (m.author == ctx.message.mentions[0]):
            await m.delete(delay=3)
        
    await asyncio.sleep(5)
    await botRecentMessage.delete(delay=3)
    await msg.delete(delay=3)
    await botQuestionMessage.delete(delay=3)

@bot.command()
async def join(ctx):
    try:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        return
    except(TypeError, AttributeError):
        await ctx.send("Either you are not in a voice channel, or I can't see the channel!")
        return

@bot.command()
async def leave(ctx):
    try:
        await ctx.voice_client.disconnect(force=True)
        return
    except(TypeError, AttributeError):
        await ctx.send("Can't disconnect from a voice channel when I'm not in one!")
        return

@bot.command()
async def say(ctx):
    message_queue = deque([])
    message = ctx.message.content[5:]
    usernick = ctx.message.author.display_name
    message = usernick + " พูดว่า " + message
    try:
        vc = ctx.message.guild.voice_client
        if not vc.is_playing():
            f = await getTTS(message)
            vc.play(discord.FFmpegPCMAudio(f, pipe=True))
        else:
            message_queue.append(message)
            while vc.is_playing():
                await asyncio.sleep(0.1)
            f = await getTTS(message_queue)
            vc.play(discord.FFmpegPCMAudio(f, pipe=True))
    except(TypeError, AttributeError):
        try:
            f = await getTTS(message)
            channel = ctx.message.author.voice.channel
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(f, pipe=True))
        except(AttributeError, TypeError):
            await ctx.send("I'm not in a voice channel and neither are you!")
        return
    f.close()

@bot.event
async def on_voice_state_update(ctx, before, after):
    channel = ctx.guild.text_channels[4]
    if before.channel != after.channel:
        embed = discord.Embed(title=f"{ctx.guild.name}", description="Leave/Join", 
                    timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
        if before.channel : embed.add_field(name="Leaved", value=f"{before.channel.mention}")
        if after.channel : embed.add_field(name="Joined", value=f"{after.channel.mention}")
        embed.set_thumbnail(url=f"{ctx.avatar_url}")
        await channel.send(embed=embed)
            

@bot.command()
async def populate(ctx):
    for i in range(10):
        await ctx.message.channel.send("Hello~" + str(i))
        asyncio.sleep(5)

@bot.command()
async def focus_on_me(ctx):
    if ctx.author.id in tts_focusing:
        await ctx.message.channel.send(str(f"I am focusing you {ctx.author.display_name}"))
        return
    if not ctx.author.voice.channel:
        await ctx.message.channel.send(str(f"{ctx.author.display_name} you are not in the voice channel."))
        return
    tts_focusing[ctx.author.id] = True 

@bot.event
async def on_message(message):
    if message.content[0:len(PREFIX)] != PREFIX and message.author != bot.user:
        print(message.guild.voice_client)
        return

    await bot.process_commands(message)

bot.run(TOKEN)