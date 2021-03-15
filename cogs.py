# Librairies
from datetime import date
import asyncpg
import datetime as dt
import discord_secret
from discord.ext import commands, tasks
from main import client
from trello_task import work_list


def setup(cli):
    cli.add_cog(CogOwner(cli))


class CogOwner(commands.Cog):
    def __init__(self, cli):
        self.cli = cli
        self.auto_archive.add_exception_type(asyncpg.PostgresConnectionError)
        self.auto_archive.start()
        self.first_card = work_list.list_cards()[0]

    @commands.command()
    async def archive(self, ctx):
        today = date.today()

        channel = client.get_channel(discord_secret.secret_channel)

        if self.first_card.due_date.strftime('%d %b %Y') == today.strftime('%d %b %Y'):
            self.first_card.delete()
            await channel.send("La carte d'aujourd'hui a été archivée")
        else:
            await channel.send("La carte d'aujourd'hui a déjà été supprimée")

    # If it's 10pm (21+1 because bad utc) archive today card
    @tasks.loop(hours=1)
    async def auto_archive(self):
        channel = client.get_channel(discord_secret.secret_channel)

        if (dt.date.today().day == self.first_card.due_date.day) and (dt.datetime.utcnow().hour == 21):
            self.first_card.delete()
            await channel.send("La carte d'aujourd'hui a été archivée automatiquement")
        else:
            pass
