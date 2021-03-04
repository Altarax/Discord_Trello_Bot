# Librairies
import discord_secret
from discord.ext import commands
from datetime import date
from trello_task import work_list
from main import client


def setup(cli):
    cli.add_cog(CogOwner(cli))


class CogOwner(commands.Cog):
    def __init__(self, cli):
        self.cli = cli

    @commands.command()
    async def archive(self, ctx):
        first_card = work_list.list_cards()[0]
        today = date.today()

        channel = client.get_channel(discord_secret.secret_channel)

        if first_card.due_date.strftime('%d %b %Y') == today.strftime('%d %b %Y'):
            first_card.delete()
            await channel.send("La carte d'aujourd'hui a été archivée")
        else:
            await channel.send("La carte d'aujourd'hui a déjà été supprimée")