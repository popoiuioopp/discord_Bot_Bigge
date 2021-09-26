import asyncio

COMMANDS = ["test", "clear", "play"]

async def on_command(words, message, mentions, client):
    if words[0] == COMMANDS[0]:
        ## TEST COMMAND ##
        print(words[1:])
        print(mentions)

    if words[0] == COMMANDS[1]:
        ## CLEAR COMMAND ##
        botQuestionMessage = await message.channel.send("Are you sure you want to clear the messages? type \"Yes or No\"")
        clearingMessage = "Clearing "

        def check(m):
            return (m.content == "Yes" or m.content == "No") and m.channel == message.channel and m.author == message.author

        try:
            msg = await client.wait_for('message', check=check, timeout=6)
        except asyncio.TimeoutError:
            await message.channel.send('👎 Timed out')

        if msg.content != "Yes":
            botRecentMessage = await message.channel.send("Okay, I won't clear the messages.")
            await asyncio.sleep(5)
            await msg.delete(delay=3)
            await botQuestionMessage.delete(delay=3)
            await botRecentMessage.delete(delay=3)
            return
        if mentions:
            if not message.author.guild_permissions.administrator and mentions[0] != message.author: 
                await message.channel.send("You don't have permission to clear messages")
                return
        
            if message.author == message.author:
                clearingMessage += "all your messages"

        clearingMessage += ".."
        botRecentMessage = await message.channel.send(clearingMessage)
        async for m in message.channel.history(limit=100):
            if m == botRecentMessage:
                continue
            if not mentions or (m.author == mentions[0]):
                await m.delete(delay=3)
            
        await asyncio.sleep(5)
        await botRecentMessage.delete(delay=3)
        await msg.delete(delay=3)
        await botQuestionMessage.delete(delay=3)

    if words[0] == COMMANDS[2]:
        ## PLAY COMMAND ##
        pass