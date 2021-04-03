# Librairies
import asyncio
import os
import discord_secret
from trello_task import work_list
from discord.ext import commands
from trello_task import get_new_card

# Scheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

client = commands.Bot(command_prefix="!")

list_information = []


# Everyday the bot is saying us that we have to work
async def notification():
    general_channel = client.get_channel(discord_secret.secret_channel_general)
    first_card_work_list = work_list.list_cards()[0]

    await general_channel.send(f"@everyone >> C'est l'heure de bosser !\n"
                               f"Aujourd'hui on fait ça < {first_card_work_list.name} >")


# Launch
@client.event
async def on_ready():
    print("I'm Ready !")

    # initializing scheduler
    scheduler = AsyncIOScheduler()

    # sends msg to the channel every day
    scheduler.add_job(notification, 'interval', hours=24, start_date='2021-04-03 19:00:00', end_date='2030-04-03 '
                                                                                                     '19:00:00')

    # starting the scheduler
    scheduler.start()


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


# Delete messagew
@client.command()
async def d(ctx, amount):
    if str(amount) == "all":
        await ctx.channel.purge(limit=1000)
    else:
        await ctx.channel.purge(limit=int(amount) + 1)


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
async def new_card_loop():
    global list_information

    while True:
        list_new_card = get_new_card()

        if list_new_card != 0:
            list_information = list_new_card
            await on_trello()

        await asyncio.sleep(2)


task = None


# Starting the loop
@client.command()
async def start(ctx):
    global task
    task = client.loop.create_task(new_card_loop())

    await d(ctx, 0)


# Stopping the loop
@client.command()
async def stop(ctx):
    task.cancel()

    await d(ctx, 0)


initial_extensions = ['cogs.first_cog',
                      'cogs.reminder']

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

    client.run(discord_secret.token)
