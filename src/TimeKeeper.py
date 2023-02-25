import discord
import asyncio
from discord.ext import tasks, commands
from OperDb import OperationDB

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', description="This is a helper bot",intents= intents)



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

def GetTimeConf():
    oData = None
    
    #look up for a rule of the timer
    oData = OperationDB('SEL', 'TIMER_RULE', ['TimeReachPres','TimeLimitPres','TimeReachQuestion','TimeLimitQuestion','TimerLimit'], None, "STATUS = 'OK'", None)
    
    for OneRow in oData:
        #print(OneRow[0],OneRow[1],OneRow[2],OneRow[3])
        nTimeReachPres = OneRow[0]#IdGame
        nTimeLimitPres = OneRow[1]#IdGame
        nTimeReachQuestion = OneRow[2]#IdGame
        nTimeLimitQuestion = OneRow[3]#IdGame
        nTimerLimit = OneRow[4]#IdGame
    
    return [oData, nTimeReachPres, nTimeLimitPres, nTimeReachQuestion, nTimeLimitQuestion, nTimerLimit]            
    
def GetGlobalVar():
    oConection = None
    oSelect = []
    oSelect = GetTimeConf()

    oConection = oSelect[0]

    global nTimeReachPres
    global nTimeLimitPres
    global nTimeReachQuestion
    global nTimeLimitQuestion
    global nTimerLimit

    nTimeReachPres = int(oSelect[1])
    nTimeLimitPres = int(oSelect[2])
    nTimeReachQuestion = int(oSelect[3])
    nTimeLimitQuestion = int(oSelect[4])
    nTimerLimit = int(oSelect[5])
    oConection.close()
#print('nTimeReachPres: ' + str(nTimeReachPres))

def Select_Role(sProcedure : str):
    GetGlobalVar()
    global nTimeReachPres
    global nTimeLimitPres
    global nTimeReachQuestion
    global nTimeLimitQuestion
    global nTimerLimit

    if sProcedure.upper() == 'P':
        return [nTimeReachPres, nTimeLimitPres]
    elif sProcedure.upper() == 'Q':
        return [nTimeReachQuestion, nTimeLimitQuestion]

def Seconds_to_TimeFormat(nSec : int):
    mins, secs = divmod(nSec, 60)
    timer = '{:02d}:{:02d}'.format(mins, secs)
    return timer

@bot.command(pass_context=True)
async def RuleTime(ctx, cProcedure : str, sUser : str):
    GetGlobalVar()
    global nTimeReachPres
    global nTimeLimitPres
    global nTimeReachQuestion
    global nTimeLimitQuestion
    global nTimerLimit    
    #print('ruletime')
    if cProcedure.upper() == 'P':
            
        timer = Seconds_to_TimeFormat(nTimeLimitPres)

        await ctx.send('INFO: Limit time of the Presentation: ' + timer + ' for ' + sUser)

    elif cProcedure.upper() == 'Q':
    
        timer = Seconds_to_TimeFormat(nTimeLimitQuestion)

        await ctx.send('INFO: Limit time of the Follows-Questions: ' + timer + ' for ' + sUser)

@bot.command(pass_context=True)
async def LastMessage(ctx, LastTime : int):  
    await ctx.send(':stopwatch:          :stopwatch:          :stopwatch:          :stopwatch:')
    await ctx.send('**TIME: ' + str(Seconds_to_TimeFormat(LastTime)) + '**')
    await ctx.send(':stopwatch:          :stopwatch:          :stopwatch:          :stopwatch:')

@bot.command(pass_context=True)
async def RuleLoop(ctx, nTime : int, sProcedure : str):
    GetGlobalVar()
    global nTimeReachPres
    global nTimeLimitPres
    global nTimeReachQuestion
    global nTimeLimitQuestion
    global nTimerLimit

    nTimeSel = Select_Role(sProcedure)
    nTimeReach = nTimeSel[0]
    nTimesUp = nTimeSel[1]
    
    if nTime == nTimeReach:#TIME IS UP! You have reached 45 Seconds.
        None
        #await ctx.send('**YOU HAVE REACHED '+ Seconds_to_TimeFormat(nTimeReach) +' seconds,** *'+ str(nTimesUp - nTimeReach) +' seconds left.*')
    if nTime == nTimesUp:
        await ctx.send('**TIMES UP! you have reached ' + Seconds_to_TimeFormat(nTimesUp) + ' ** *and continues the time.*')  

    #Stop the timer when reached the limit of time.
    if nTime == nTimerLimit:
        await ctx.send('**TIME: ' + str(Seconds_to_TimeFormat(nTime)) + '**')
        slow_count.stop()

@tasks.loop(seconds=1.0)
async def slow_count(ctx, sProcedure):
    #print('Procedure: ' + sProcedure)
    print(slow_count.current_loop)
    #procedure wich analize the time and send messages
    await RuleLoop(ctx, slow_count.current_loop, sProcedure)

@slow_count.before_loop
async def before_printer():
    print('waiting...')

@slow_count.after_loop
async def after_slow_count():
    #Here put all code after finish the loop
    print('done!')

@bot.command(pass_context=True)
async def starttimer(ctx, sProcedure : str, sUser : str):    
    await RuleTime(ctx, sProcedure, sUser)
    await slow_count.start(ctx, sProcedure)
    

@bot.command(pass_context=True)
async def stoptimer(ctx) -> int:
    slow_count.stop()
    LastTime = slow_count.current_loop
    await LastMessage(ctx, slow_count.current_loop)
    return LastTime

#Events
'''
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Three Questions' Game",url=""))
    print("My Bot is ready")
'''
