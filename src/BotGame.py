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

    class ChannelDetail():
        def __init__(self, ChannelId, ChannelName):
            self.ChannelId = ChannelId
            self.ChannelName = ChannelName            
    
    def __init__(self, bot):
        self.bot = bot  
        self.MyChannel = []
        
        self.MyChannel.append(self.ChannelDetail('1071493291876552872', 'Lounge'))
        self.MyChannel.append(self.ChannelDetail('1071493292363087964', 'Study Room 1'))
        self.MyChannel.append(self.ChannelDetail('1071493292363087965', 'Study Room 2'))
                    

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
        cIdChannel = '1071493291876552872'

        oData = OperationDB('SEL', 'GAME', ['IDGAME'], None, "STATUS = 'OK' and IDCHANNEL = '" + str(cIdChannel) + "'")        
        
        for OneRow in oData:            
            nIdGame = OneRow[0]#IdGame
        return [nIdGame, oData]
    '''
    @commands.Cog.listener()
    async def get_channel(self, ctx, *, given_name=None):
        for channel in ctx.guild.channels:
            if channel.name == given_name:
                wanted_channel_id = channel.id  

        return wanted_channel_id
    '''
    def Get_MemberId(self, cMemberId: str):
        nIdMember = []
        oSelect = self.Get_Game_OK()#find a active game
        nIdGame = oSelect[0]
        oConection = oSelect[1]
        oConection.close()

        oData = OperationDB('SEL', 'DISCORD_USER', ['IDMEMBER'], None, "IDMEMBER = '" + cMemberId + "' and IDGAME = " + str(nIdGame))
        
        for OneRow in oData:            
            nIdMember = OneRow[0]#IdGame    

        oData.close()
        return [nIdMember, oData]
    
    def GetChannelId(self, cChannelName: str) -> str:
        cChannel = ''
        for i in range(len(self.MyChannel)):
            if cChannelName == str(self.MyChannel[i].ChannelName):
                cChannel = self.MyChannel[i].ChannelId
                return cChannel
            #print('Class myChannel -> Channel Id: ' + str(foo.MyChannel[i].ChannelId) + ' Name: ' + str(foo.MyChannel[i].ChannelName)) 

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
        print('all members')

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
            
            oSelect = []
            oSelect = self.Get_MemberId(str(MyMember[i].MemberId))#Find is a member exists in the table: DISCORD_USER
            nMemberId = oSelect[0]
            oConection = oSelect[0]
            
            if len(nMemberId) == 0:
                #Insert a row of a game of a Channel Room
                OperationDB('INS', 'DISCORD_USER', ['IDMEMBER','IDGAME','IDCHANNEL','USERDESC','DATEREG','HELPER','PLAYER','STATUS'], ["'" + str(MyMember[i].MemberId) + "'" , str(nIdGame) , "'" + str(cIdChannel) + "'", "'" + str(MyMember[i].MemberName) + "'" , "'" + self.Get_Time() + "'" , "'N'", "'Y'", "'OK'"], None)

            oConection.close()
#def setup(bot):#register the Cog
#    bot.add_cog(Events(bot))  

@bot.event
async def on_ready():
    print('on_ready')
    print('We have logged in as {}'.format(bot.user))

#@bot.command()
@bot.event
async def on_voice_state_update(member:discord.Member, before, after): 
    #Global: cMemberId
    cMemberId = member.id

    if member == bot.user:  #CATCH
        return
    
    if str(after.channel) == 'Lounge':
        print('channel: ' + str(before.channel) + ' - ' + str(after.channel) + ' Id Channel: ' + str(foo.GetChannelId(str(after.channel))))
        #print('mute: ' + str(after.self_mute))

    #foo.GetChannelId()


    if after.channel is not None:#only the code run if the channel is the channel's game
        if str(after.channel) != 'Lounge':
            return
    elif before.channel is not None:
        if str(before.channel) != 'Lounge':
            return

    if before.channel is not None: #User has left a voice channel
        print(f'{member.id} User left voice channel')
        #print(f'{member} Joined Channel')

        cMemberId = member.id

        #print('Member Left voice channel: ' + cMemberId[0])

        print('Member id: ' + str(cMemberId))

        oSelect = []
        oSelect = foo.Get_Game_OK()#find a active game
        
        nIdGame = oSelect[0]
        oConection = oSelect[1]
        
        print('event before oConection.rowcount: ' + str(oConection.rowcount))
        
        oSelect = []
        oSelect = foo.Get_MemberId(str(member.id))#find a member from DISCORD_USER's table
        nIdMember = oSelect[0]
        oConection = oSelect[1]        

        if len(nIdMember) > 0:

            #update the state's user in the table DISCORD_USER to OUT
            OperationDB('UPD', 'DISCORD_USER', "STATUS = 'OUT'", None, "IDMEMBER = '" + str(member.id) + "' and IDGAME = " + str(nIdGame))             
        
        oConection.close()
       
        return

    elif after.channel is not None: #User has left a voice channel
        
        #if before.channel is not after.channel:
        cMemberId = member.id

        memids = []
        VC = member.voice.channel

        for mem in VC.members:
            memids.append(mem.id)

        if len(memids) > 0:
            #await asyncio.sleep(5)  #to be 10
            print(len(memids))
            if len(memids) > 0:
                #await VC.connect()
                print(f'{member} Joined Channel')

                oSelect = []
                oSelect = foo.Get_Game_OK()#find a active game
                nIdGame = oSelect[0]
                oConection = oSelect[1]

                oConection.close()

                oSelect = []
                oSelect = foo.Get_MemberId(str(member.id))
                nIdMember = oSelect[0]
                oConection = oSelect[1]  

                print('member id from select: ' + str(nIdMember))
                print('total rows from select: ' + str(len(nIdMember)))
                
                #if oData.rowcount() > 0:
                if len(nIdMember) > 0:

                    #update the state's user in the table DISCORD_USER to OK
                    OperationDB('UPD', 'DISCORD_USER', "STATUS = 'OK'", None, "IDMEMBER = '" + str(memids[0]) + "' and IDGAME = " + str(nIdGame))                          
                    print('Member in DISCORD_USER: ' + nIdMember)

                elif len(nIdMember) <= 0:
                    
                    cIdChannel = str(foo.GetChannelId(str(after.channel)))#find the ChannelId

                    #Insert a member into the game
                    OperationDB('INS', 'DISCORD_USER', ['IDMEMBER','IDGAME','IDCHANNEL','USERDESC','DATEREG','HELPER','PLAYER','STATUS'], ["'" + str(member.id) + "'" , str(nIdGame) , "'" + str(cIdChannel) + "'", "'" + str(member.name) + "'" , "'" + foo.Get_Time() + "'" , "'N'", "'Y'", "'OK'"], None)

                oConection.close()
                #print(f'{member} has joined the vc')
            else:
                print("Not Alone Anymore...")
                return
        else:
            print("Does exists members into the room")
            return #Leave voice channel
        
    return

@bot.event
async def on_interaction(interaction):
    #if str(interaction.type) == "InteractionType.application_command":
    print("test interactions")


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

@bot.command()
async def run_allmembers(ctx):
    print('dentro run_allmembers')
    await run_allmembers2(ctx)

async def run_allmembers2(ctx):
    await foo.allmembers(ctx)#member=discord.member



bot.run(format(env['BOT_TOKEN']))