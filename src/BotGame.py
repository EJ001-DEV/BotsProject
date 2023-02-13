import discord
from discord.ext import commands
from datetime import datetime
from timer import Timer, TimerStatus

#################################
#Both library to gets values from .env file
from dotenv import load_dotenv
from os import environ as env
#################################

from OperDb import OperationDB
import os

load_dotenv()


intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', description="This is a helper bot",intents= intents)


class Events(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
            print('event')

        @commands.Cog.listener()
        async def on_ready(self):
            print('Ready!')
            print('Logged in as ---->', self.bot.user)
            print('ID:', self.bot.user.id)

        @commands.Cog.listener()
        async def on_message(self, message):
            print(message)            

class OperDiscord(commands.Cog):

    class MemberDetail():
        def __init__(self, MemberId, MemberName, ChannelRoomId):
            self.MemberId = MemberId
            self.MemberName = MemberName
            self.ChannelRoomId = ChannelRoomId
    
    
    def __init__(self, bot):
        self.bot = bot  
        print('init')
        #intents = discord.Intents.all()
        #intents.message_content = True
        #intents.members = True

        #self.bot = commands.Bot(command_prefix='!', description="This is a helper bot",intents= intents)      

    #@commands.Cog.listener()
    #async def on_ready(self):
    #    print('on_ready')
    #    print('We have logged in as {}'.format(self.bot.user))
    #    await self.bot.change_presence(activity=discord.Streaming(name="Three Questions' Game",url=""))

    def Get_Time(self):
        now = datetime.now()        
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return current_time

    def Get_Game_OK(Self):
        cIdChannel = '1072469507504873492'

        oData = OperationDB('SEL', 'GAME', ['IDGAME'], None, "STATUS = 'OK' and IDCHANNEL = '" + str(cIdChannel) + "'")        
        
        for OneRow in oData:            
            nIdGame = OneRow[0]#IdGame
        return nIdGame

    def Get_MemberId(self, cMemberId: str):
        nIdGame = self.Get_Game_OK()#find a active game

        oData = OperationDB('SEL', 'DISCORD_USER', ['IDMEMBER'], None, "IDMEMBER = '" + cMemberId + "' and IDGAME = " + str(nIdGame))
        
        for OneRow in oData:            
            nIdMember = OneRow[0]#IdGame    

        oData.close()
        return nIdMember            

    @commands.Cog.listener()
    async def startgame(self, ctx):
        """
        Start the Three Questions' Game

        Example: !startgame
        """
        #member = ctx.author
        print('start game')
        cIdChannel = '1072469507504873492'
        #channel = bot.get_channel(1071493291876552872)

        print('guild: ' + str(ctx.guild.id) + ' author: ' , ctx.author)
        #'Channel: ' + str(ctx.channel.id)
        oData = OperationDB('SEL', 'GAME', ['IDGAME'], None, "STATUS = 'OK' and IDCHANNEL = '" + cIdChannel + "'")
        '''
        for row in oData:
            #print(row[0] , row[1], row[2])        
            print(row)'''
        #print(len(oData.fetchall()))
        print('Total of rows: ' + str(len(oData.fetchall())))
        
        if len(oData.fetchall()) < 0:#verifying if the table is empty
            print('Tabla vacia')
            now = datetime.now()        
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            
            #Insert a row of a game of a Channel Room
            OperationDB('INS', 'GAME', ['IDCHANNEL','DATESTARTGAME','DESCRIPTION','STATUS'], ["'"+ cIdChannel + "'", "'"+ current_time + "'", "'TQD game'", "'OK'"], '')
        else:#show a meesage in Discord
            await ctx.send('Game have been started, to stop the game type: !stopgame')
        oData.close()
        
        #await self.allmembers(ctx)#list all members of Channel Room
    
    @commands.Cog.listener()
    async def allmembers(self, ctx):#, member : discord.member
        cIdChannel = 1072469507504873492
        MyMember = []
        channel = self.bot.get_channel(cIdChannel) 

        members = channel.members

        print(channel)
        print(members)

        oData = OperationDB('SEL', 'GAME', ['IDGAME'], None, "STATUS = 'OK' and IDCHANNEL = '" + str(cIdChannel) + "'")        
        
        for OneRow in oData:
            nIdGame = OneRow[0]#IdGame

        print('IdGame: ' + str(nIdGame))
        
        oData.close()

        MyMember = []
        
        for member in members:
            MyMember.append(self.MemberDetail(member.id, member.name, channel.id))

        for i in range(len(MyMember)):
            print('Channel Id: ' + str(MyMember[i].ChannelRoomId) + ' id: ' + str(MyMember[i].MemberId) + ' User: ' + str(MyMember[i].MemberName))
            
            nMemberId = self.Get_MemberId(str(MyMember[i].MemberId))#Find is a member exists in the table: DISCORD_USER
            
            if len(nMemberId) == 0:
                #Insert a row of a game of a Channel Room
                OperationDB('INS', 'DISCORD_USER', ['IDMEMBER','IDGAME','IDCHANNEL','USERDESC','DATEREG','HELPER','PLAYER','STATUS'], ["'" + str(MyMember[i].MemberId) + "'" , str(nIdGame) , "'" + str(cIdChannel) + "'", "'" + str(MyMember[i].MemberName) + "'" , "'" + self.Get_Time() + "'" , "'N'", "'Y'", "'OK'"], None)
        
#def setup(bot):#register the Cog
#    bot.add_cog(Events(bot))  

@bot.event
async def on_ready():
    print('on_ready')
    print('We have logged in as {}'.format(bot.user))

#@bot.command()
@bot.event
async def on_voice_state_update(member:discord.Member, before, after):
    cIdChannel = 1072469507504873492
    if member == bot.user:  #CATCH
        return
    
    print('channel: ' + str(before.channel) + ' - ' + str(after.channel))

    if after.channel is not None:#only the code run if the channel is the channel's game
        if str(after.channel) != 'Lounge':
            return
    elif before.channel is not None:
        if str(before.channel) != 'Lounge':
            return

    if after.channel is None: #User has left a voice channel
        print(f'{member.id} User left voice channel')
        #print(f'{member} Joined Channel')

        cMemberId = member.id

        #print('Member Left voice channel: ' + cMemberId[0])

        print('Member id: ' + str(cMemberId))

        nIdGame = foo.Get_Game_OK()#find a active game

        #update the state's user in the table DISCORD_USER to OUT
        OperationDB('UPD', 'DISCORD_USER', "STATUS = 'OUT'", None, "IDMEMBER = '" + str(cMemberId) + "' and IDGAME = " + str(nIdGame))             

        return

    else:
        if before.channel is not after.channel:
            memids = []
            VC = member.voice.channel

            for mem in VC.members:
                memids.append(mem.id)

            if len(memids) == 1:
                #await asyncio.sleep(5)  #to be 10
                print(len(memids))
                if len(memids) == 1:
                    #await VC.connect()
                    print(f'{member} Joined Channel')

                    nIdGame = foo.Get_Game_OK()#find a active game

                    oData = OperationDB('SEL', 'DISCORD_USER', ['IDMEMBER'], None, "IDMEMBER = '" + str(memids[0]) + "' and IDGAME = " + str(nIdGame))
                    
                    for OneRow in oData:            
                        nIdMember = OneRow[0]#IdGame
                    #print('member id from select: ' + str(oData.rowcount))
                    
                    if oData.rowcount > 0:
                        #update the state's user in the table DISCORD_USER to OK
                        OperationDB('UPD', 'DISCORD_USER', "STATUS = 'OK'", None, "IDMEMBER = '" + str(memids[0]) + "' and IDGAME = " + str(nIdGame))                          
                        print('Member in DISCORD_USER: ' + nIdMember)
                    elif oData.rowcount < 0:
                        None#create a user
                        
                        #await foo.allmembers(ctx)
                        #run_allmembers(ctx)

                    oData.close()
                    #print(f'{member} has joined the vc')
                else:
                    print("Not Alone Anymore...")
                    return
            else:
                print("!=1")
                #Leave voice channel

        else:
            return
        return
    return



# --- main ---





#setup(bot)

foo = OperDiscord(commands.Cog)#Instans a class

#@foo.bot.command()
@bot.command()
async def OperGame(ctx):
    """
    Start the Three Questions' Game

    Example: !startgame
    """
    #member = ctx.author
    #fEvent = Events(commands.Cog)
    #await setup(foo.bot)

    #await foo.allmembers(ctx)#member=discord.member
    #await setup(bot)#register the Cog and Events to work
    await foo.startgame(ctx)

#@bot.command()
@bot.command()
async def run_allmembers(ctx):
    await foo.allmembers(ctx)#member=discord.member



bot.run(format(env['BOT_TOKEN']))