import discord
import asyncio
from discord.ext import tasks, commands


intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='>', description="This is a helper bot",intents= intents)

class MyCog(commands.Cog):
    def __init__(self):
        self.bot= bot
        self._batch = []
        self.lock = asyncio.Lock()
        self.bulker.start()        
        self.index = 0
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=10.0)
    async def bulker(self):
        async with self.lock:
            await self.do_bulk()

    @tasks.loop(seconds=5.0)
    async def printer(self):
        print(self.index)
        self.index += 2

    @printer.before_loop
    async def before_printer(self):
        print('waiting...')
        await self.bot.wait_until_ready()

    @tasks.loop(minutes=5.0)
    async def batch_update(self):
        async with self.bot.pool.acquire() as con:
            # batch update here...
            pass

    @bulker.after_loop
    async def on_bulker_cancel(self):
        if self.bulker.is_being_cancelled() and len(self._batch) != 0:
            # if we're cancelled and we have some data left...
            # let's insert it to our database
            await self.do_bulk()

'''def ProStop():
    slow_count.clear_exception_types()
    slow_count.stop()'''
    
@tasks.loop(seconds=5.0, count=5)
async def slow_count():
    print(slow_count.current_loop)

@slow_count.before_loop
async def before_printer():
    print('waiting...')

@slow_count.after_loop
async def after_slow_count():
    print('done!')

@bot.command()
async def start(ctx):
    await slow_count.start()

@bot.command()
async def stop(ctx):    
    slow_count.clear_exception_types()
    slow_count.stop()     



#Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Tutorials",url="http:/www.youtube.com"))
    print("My Bot is ready")

       


bot.run('MTA3MTU2MzkxMzI0MzY2ODU3MA.Ge86lU.s-w4u3QHqcIRWXAnoQSh3OTkukTJghlPHhtDc8')