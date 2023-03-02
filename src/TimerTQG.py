import discord
from discord.ext import commands

#################################
#Both library to gets values from .env file
from dotenv import load_dotenv
from os import environ as env
#################################

from TimeKeeper import starttimer, stoptimer


load_dotenv()


intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', description="This is a helper bot",intents= intents)

cFunctionName = ''

@bot.command()
async def start(ctx, cProcedure: str, cUser: str):#start timer

    await starttimer(ctx, cProcedure, cUser)
    

@bot.command()
async def stop(ctx):#Sop Timer

    #cMember = member:discord.Member
    LastTime = await stoptimer(ctx)
    
    print('LastTime: ' + str(LastTime))
    #print('cProcedureGloba: ' + cProcedureGlobal)    

bot.run(format(env['BOT_TEST']))#Start the Bot        