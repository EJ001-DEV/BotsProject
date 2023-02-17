import discord
from discord.ext import commands

#################################
#Both library to gets values from .env file
from dotenv import load_dotenv
from os import environ as env
#################################

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', description="This is a helper bot",intents= intents)

cFunctionName = ''

def my_decorator(func):
    def wrapper(*args, **kwargs):
        global cFunctionName
        
        print(f"The function name is: {func.__name__}")

        if func.__name__ == 'foo':
            cFunctionName = func.__name__
            #return

        return func(*args, **kwargs)
    return wrapper
 
 
@my_decorator
async def foo(ctx):
    global cFunctionName
    #print("Autor: " + str(ctx.author))
    print("Member: " + str(ctx.author.id))
    
    print('cFunctionName: ' + str(cFunctionName))
    print("Inside foo")
    await ctx.send('Dentro de foo')
 
#bot.get_user()
#
@bot.command()
async def foo2(ctx):
    await foo(ctx)

bot.run(format(env['BOT_TOKEN']))#Start the Bot