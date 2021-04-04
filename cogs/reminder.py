# Librairies
from apscheduler.schedulers.blocking import BlockingScheduler
from discord.ext import commands
import discord_secret
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main import client, d

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

        reminder_final_dict = {}

        for key, value in reminders_1d.items():
            if value not in reminder_final_dict:
                reminder_final_dict[value] = [key]
            else:
                reminder_final_dict[value].append(key)

        for user in reminder_final_dict.keys():
            await reminder_channel.send(f"@{str(user)} Je devais te rappeler : \n"
                                        f"{str(reminder_final_dict.get(user)).replace('dict_values', '').replace('(', '').replace(')', '').replace('[', '').replace(']', '')}")

        reminder_final_dict.clear()
        reminders_1d.clear()

    @commands.Cog.listener()
    async def every_week(self):
        reminder_channel = self.cli.get_channel(discord_secret.secret_reminder_channel)

        reminder_final_dict = {}

        for key, value in reminders_1w.items():
            if value not in reminder_final_dict:
                reminder_final_dict[value] = [key]
            else:
                reminder_final_dict[value].append(key)

        for user in reminder_final_dict.keys():
            await reminder_channel.send(f"@{str(user)} Je devais te rappeler : \n"
                                        f"{str(reminder_final_dict.values()).replace('dict_keys', '').replace('(', '').replace(')', '').replace('[', '').replace(']', '')}")

        reminder_final_dict.clear()
        reminders_1w.clear()

    @client.command()
    async def rappel(self, ctx, interval, *args):
        reminder = " ".join(args[:])

        if str(interval) == "1d":
            reminders_1d[reminder] = ctx.message.author.name
            await d(ctx, 0)
        else:
            pass

        if str(interval) == "1w":
            reminders_1w[reminder] = ctx.message.author.name
            await d(ctx, 0)
        else:
            pass

    @client.command()
    async def test(self, ctx):
        print(reminders_1d)
        print(reminders_1w)


def setup(cli):
    cli.add_cog(Reminder(cli))
