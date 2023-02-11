import discord
from discord.ext import commands
#################################
#Both library to gets values from .env file
from dotenv import load_dotenv
from os import environ as env
#################################

from OperDb import OperationDB
import os

load_dotenv()

class OperDiscord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    
        intents = discord.Intents.all()
        intents.message_content = True

        self.bot = commands.Bot(command_prefix='!', description="This is a helper bot",intents= intents)        

    @commands.Cog.listener()
    #@commands.Bot.event(commands.Bot)
    #@commands.Bot.event
    async def on_ready(self):
        print('on_ready')
        print('We have logged in as {}'.format(self.bot.user))
        await self.bot.change_presence(activity=discord.Streaming(name="Three Questions' Game",url=""))
    
    #member:discord.Member
    #@commands.command(pass_context=True)
    @commands.Cog.listener()
    #@commands.Bot.command()
    async def startgame(self, ctx):
        #member = ctx.author
        print('start game')
        print('guild: ' + str(ctx.guild.id) + ' author: ', ctx.author)


foo = OperDiscord(commands.Cog)


@foo.bot.command()
async def OperGame(ctx):
    #member = ctx.author
    await foo.startgame(ctx)
'''
oData = OperationDB('SEL', 'VOICE_CHANNEL', ['IDCHANNEL','CHANNELNAME'], None, "IDCHANNEL = '1071493291876552872'")

for i in oData:
    print(i)
oData.close()
'''

foo.bot.run(format(env['BOT_TOKEN']))

#oOperDB.ProcSelect('channel2', ['id','username','delay'], "username = 'EJ001'")