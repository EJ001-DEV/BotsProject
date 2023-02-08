import discord
from discord.ext import commands
import datetime
import time
import asyncio

from urllib import parse, request
import re

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='>', description="This is a helper bot",intents= intents)

def seconds_to_timeFormat(ctx, nSec:int):
    mins, secs = divmod(nSec, 60)
    timer = '{:02d}:{:02d}'.format(mins, secs)
    return timer

#bot = commands.Bot(command_prefix="!")


counter_channel = '*'
task = None
bStopWatch = False

#@bot.command(pass_context=True)
# define the countdown func.
async def timekeeper(ctx, sUser: str, sProc: str):
    
    global counter_channel
    global bStopWatch
    
    #print('counter_channel: ' + counter_channel)
    #print('task: ' + task)
    print('bStopWatch: ' + str(bStopWatch))

    if bot.loop.is_closed():
        print('Task cerrada')
            
    cProcedure = sProc

    t = 1
    nCounterTime = 0 
    
    if cProcedure.upper() == 'P':
        nTimeReach = 50
        nTimesUp = 65
        
        timer = seconds_to_timeFormat(ctx, nTimesUp)

        await ctx.send('Limit time of the Presentation: ' + timer + ' for ' + sUser)

    elif cProcedure.upper() == 'Q':
        nTimeReach = 30
        nTimesUp = 45

        timer = seconds_to_timeFormat(ctx, nTimesUp)

        await ctx.send('Limit time of the Follows-Questions: ' + timer + ' for ' + sUser)


    while t <= 300:# or cProcedure.upper() == 'Q' and t == nTimesUp:
        mins, secs = divmod(t, 60)
        
        #timer = '{:02d}:{:02d}'.format(mins, secs)   
        timer = seconds_to_timeFormat(ctx, t) 
        #await message.send(timer)
        #await ctx.send(timer)
        #print(timer, end="\r")        
        time.sleep(1)
        
        print(timer)
        
        if bStopWatch:
            await ctx.send('**TIME: ' + timer + '**')  
            return

        if t == nTimeReach:#TIME IS UP! You have reached 45 Seconds.
            #await ctx.send('**'+ sUser +' has reached '+ str(nTimeReach) +' Seconds, '+ str(nTimesUp - nTimeReach) +' seconds left.**')
            await ctx.send('**TIME IS UP!** You have reached '+ str(nTimeReach) +' seconds, *'+ str(nTimesUp - nTimeReach) +' seconds left.*')
        if t == nTimesUp:
            #await ctx.send('** ( '+ timer +' ) TIMES UP! ' + sUser + ' and continues the time.**')
            await ctx.send('**TIMES UP!** *and continues the time.*')
            #nCounterTime = nTimesUp + 10
            
        #if t == nCounterTime:
        #    nCounterTime += 10
        #print('task: ' + task)
  

        t += 1
    
    

@bot.command(pass_context=True)
async def start(ctx, sUser: str, sProc: str):
    global task    
    global bStopWatch
    task = bot.loop.create_task(timekeeper(ctx, sUser, sProc))

@bot.command(pass_context=True)
async def stop(ctx):
    global task, counter_channel, bStopWatch
    print('cancel')
    bStopWatch = True
    task.cancel()


    
    task = None
    counter_channel = None  


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def sum(ctx, numOne: int, NumTwo: int):
    await ctx.send(numOne + NumTwo)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Lorem impsum asdasd", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")

    embed.add_field(name="Server owner at", value=f"{ctx.guild.owner}")

    #embed.add_field(name="Server region", value=f"{ctx.guild.region}")

    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")

    #embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(url="https://w7.pngwing.com/pngs/985/314/png-transparent-learning-python-programming-language-computer-programming-python-logo-text-computer-logo.png")

    await ctx.send(embed=embed)

@bot.command()
# define the countdown func.
async def timek(ctx, sUser: str, t: int):
    
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        #print(timer, end="\r")
        time.sleep(1)
        t -= 1
        await ctx.send(timer)
    await ctx.send('**TIMES UP '+sUser+'**')
    #print('**TIMES UP**')

@bot.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query':search})
    #print(query_string)
    html_content = request.urlopen('https://www.youtube.com/results?' + query_string)    
    search_results = re.findall(r'/watch\?v=(.{11})',html_content.read().decode())    
    await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])
    #print(search_results)


#Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Tutorials",url="http:/www.youtube.com"))
    print("My Bot is ready")

'''
@bot.event
async def on_reaction_add():
    if reaction.emoji == "😆":
        await reaction.remove()
'''


          


bot.run('MTA3MTU2MzkxMzI0MzY2ODU3MA.GusjIc.fdkFIKKS9A-TbAuyfHKtGKbhUp8xC6pUzoFXHA')