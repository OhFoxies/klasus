from utils import *
from logs import logs_
from database.connect_to_database import connect
import nextcord as discord
from nextcord.ext import commands
import asyncio
from background_tasks.LuckyNumber import lucky_number
from scheduler.asyncio import Scheduler
import datetime as dt


# noinspection PyTypeChecker
class Klasus(commands.Bot):
    def __init__(self, *, intents_: discord.Intents):
        super().__init__(intents=intents_, activity=discord.Game(config['activity']))
        self.bg_task = self.loop.create_task(self.lucky_number_info())

    async def lucky_number_info(self):
        await self.wait_until_ready()
        schedule = Scheduler()
        schedule.once(dt.time(hour=7, minute=0), lucky_number, args=(self,))
        while not self.is_closed():
            await asyncio.sleep(1)

    def start_bot(self):
        logs_.log("Staring bot.")
        connect()
        load_cogs(self)
        self.run(config["token"])


if __name__ == "__main__":
    intents: discord.Intents = discord.Intents.default()
    intents.all()
    client: Klasus = Klasus(intents_=intents)
    client.start_bot()
