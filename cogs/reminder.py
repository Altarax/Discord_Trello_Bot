# Créer une commande !reminder : Check
# Params : interval, le rappel : Check
# Créer des listes en fonction des intervals : Check
# Créer des scheduler en fonction de chaque interval
# Renvoyer dans le channel "rappels"

# Librairies
from apscheduler.schedulers.blocking import BlockingScheduler
from discord.ext import commands
import discord_secret
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main import client

reminders_1d = {}
reminders_1w = {}


class Reminder(commands.Cog):
    def __init__(self, cli):
        self.cli = cli

        # initializing scheduler
        scheduler = AsyncIOScheduler()

        # sends msg to the channel every day
        scheduler.add_job(self.every_day, 'interval', hours=24, start_date='2021-04-04 09:00:00',
                          end_date='2030-04-03 '
                                   '19:00:00')

        # sends msg to the channel every day
        scheduler.add_job(self.every_week, 'interval', weeks=1, start_date='2021-04-06 09:00:00',
                          end_date='2030-04-03 '
                                   '19:00:00')

        # starting the scheduler
        scheduler.start()

    @commands.Cog.listener()
    async def every_day(self):
        reminder_channel = self.cli.get_channel(discord_secret.secret_reminder_channel)

        for user in reminders_1d.values():
            await reminder_channel.send(f"@{user} Je devais te rappeler : \n"
                                        f"{str(reminders_1d.keys()).replace('dict_keys', '').replace('(', '').replace(')', '').replace('[', '').replace(']', '')}")

        reminders_1d.clear()

    @commands.Cog.listener()
    async def every_week(self):
        reminder_channel = self.cli.get_channel(discord_secret.secret_reminder_channel)

        for user in reminders_1w.values():
            await reminder_channel.send(f"@{user} Je devais te rappeler : \n"
                                        f"{str(reminders_1w.keys()).replace('dict_keys', '').replace('(', '').replace(')', '').replace('[', '').replace(']', '')}")

        reminders_1w.clear()

    @client.command()
    async def rappel(self, ctx, interval, *args):
        reminder = " ".join(args[:])

        if str(interval) == "1d":
            reminders_1d[reminder] = ctx.message.author.name
        else:
            pass

        if str(interval) == "1w":
            reminders_1w[reminder] = ctx.message.author.name
        else:
            pass

    @client.command()
    async def test(self, ctx):
        print(reminders_1d)
        print(reminders_1w)


def setup(cli):
    cli.add_cog(Reminder(cli))
