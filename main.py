# Librairies
import asyncio
import discord
import time
import discord_secret
from discord.ext import commands
from trello_task import get_new_card

client = commands.Bot(command_prefix="!")

list_information = []


# Launch
@client.event
async def on_ready():
    print("I'm Ready !")


# Load
@client.command()
async def load(ctx, name=None):
    if name:
        client.load_extension(name)
        await ctx.send("Extension chargée")


# Unload
@client.command()
async def unload(ctx, name=None):
    if name:
        client.unload_extension(name)
        await ctx.send("Extension déchargée")


# Reload
@client.command()
async def reload(ctx, name=None):
    if name:
        try:
            client.reload_extension(name)
            await ctx.send("Extension rechargée")
        except:
            client.load_extension(name)


# Delete message
@client.command()
async def d(ctx, amount=3):
    await ctx.channel.purge(limit=amount)


# Send message when we add a card in trello
@client.command()
async def on_trello():
    global list_information

    channel = client.get_channel(discord_secret.secret_channel)

    title = str("""```fix\n< Nouvelle carte Trello >```""")

    message = f"{title} \n" \
              f"> **{list_information[1]}** \n" \
              f"> **Date : {list_information[2].strftime('%d %b %Y')} ** "
    await channel.send(message)


# While loop to verify if we had a new card in Trello
@client.event
async def everytime():
    global list_information

    while True:
        list_new_card = get_new_card()
        if list_new_card != 0:
            list_information = list_new_card
            await on_trello()
        await asyncio.sleep(2)


client.loop.create_task(everytime())
client.run(discord_secret.token)