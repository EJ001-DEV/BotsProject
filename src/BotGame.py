import discord
from discord.ext import commands
import datetime
#import time
from datetime import datetime
#from timer import Timer, TimerStatus

#from urllib import parse, request


#################################
#Both library to gets values from .env file
from dotenv import load_dotenv
from os import environ as env
#################################

from OperDb import OperationDB
from TimeKeeper import starttimer, stoptimer
#import os

load_dotenv()


intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', description="This is a helper bot",intents= intents)


class Events(commands.Cog):
        def __init__(Self, bot):
            Self.bot = bot
            print('event')

        @commands.Cog.listener()
        async def on_ready(Self):
            print('Ready!')
            print('Logged in as ---->', Self.bot.user)
            print('ID:', Self.bot.user.id)

        @commands.Cog.listener()
        async def on_message(Self, message):
            print(message)            

class OperDiscord(commands.Cog):

    class MemberDetail():
        def __init__(Self, MemberId, MemberName, ChannelRoomId):
            Self.MemberId = MemberId
            Self.MemberName = MemberName
            Self.ChannelRoomId = ChannelRoomId

    class ChannelDetail():
        def __init__(Self, ChannelId, ChannelName):
            Self.ChannelId = ChannelId
            Self.ChannelName = ChannelName
    
    class ScoreCardDetail():
        def __init__(Self, IdMember, UserDesc, nPointTotal):
            Self.IdMember = IdMember
            Self.UserDesc = UserDesc
            Self.nPointTotal = nPointTotal

    class UserRoleDetail():
        def __init__(Self, RoleId, BotCommand):
            Self.RoleId = RoleId
            Self.BotCommand = BotCommand

    def __init__(Self, bot):
        Self.bot = bot  
        Self.MyChannel = []
        
        Self.MyChannel.append(Self.ChannelDetail('1071493291876552872', 'Lounge'))
        Self.MyChannel.append(Self.ChannelDetail('1071493292363087964', 'Study Room 1'))
        Self.MyChannel.append(Self.ChannelDetail('1071493292363087965', 'Study Room 2'))
                    

        #print('init')
        #intents = discord.Intents.all()
        #intents.message_content = True
        #intents.members = True

        #Self.bot = commands.Bot(command_prefix='!', description="This is a helper bot",intents= intents)      
    #def __str__(Self) -> str:
        
    #    return super().__str__()

    #@commands.Cog.listener()
    #async def on_ready(Self):
    #    print('on_ready')
    #    print('We have logged in as {}'.format(Self.bot.user))
    #    await Self.bot.change_presence(activity=discord.Streaming(name="Three Questions' Game",url=""))

    async def PostGeneralInfo(Self, ctx, cHeader: str, DescHeader: str, oField):
        embed = discord.Embed(title=cHeader, description=DescHeader, color=discord.Color.blue())

        embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvlJsqbDBYjobCSePQghhuHn6Ph5eDhQql6Q&usqp=CAU")

        for row in oField:
            #print('row[0]: ' + row)
            embed.add_field(name=row , value="")

        await ctx.send(embed=embed)        
        

    def Get_Time(Self):
        now = datetime.now()        
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return current_time

    def Get_Game_OK(Self) -> list:
        MyChannel = Self.MyChannel
        cIdChannel = MyChannel[0].ChannelId
        #print('MyChannel: ' + MyChannel[0].ChannelId)
        #cIdChannel = MyChannel.

        nIdGame = []
        cGameDescription = []

        oData = OperationDB('SEL', 'GAME', ['IDGAME', 'DESCRIPTION'], None, "STATUS = 'OK' and IDCHANNEL = '" + str(cIdChannel) + "'", None)        
        
        for OneRow in oData:            
            nIdGame = OneRow[0]#IdGame
            cGameDescription = OneRow[1]#IdGame
        return [oData, nIdGame, cGameDescription]

    def Get_GameStatus(Self) -> bool:
        MyChannel = Self.MyChannel        
        cIdChannel = MyChannel[0].ChannelId
        #print('MyChannel: ' + MyChannel[0].ChannelId)
        #cIdChannel = MyChannel.

        cStatus = ''
        
        oData = OperationDB('SEL', 'GAME', ['STATUS'], None, "STATUS = 'OK' and IDCHANNEL = '" + str(cIdChannel) + "'", None)        
        
        for OneRow in oData:            
            cStatus = str(OneRow[0])#GameStatus
        
        print('status: ' + cStatus)

        oData.close()
        if cStatus == 'OK':
            return True
        elif cStatus == 'END':
            return False
        elif len(cStatus) <= 0:
            return False
        

    def Get_MemberId(Self, cMemberId: str) -> list:
        nIdMember = []
        cUserDesc = []
        oSelect = []
        oSelect = Self.Get_Game_OK()#find a active game
        oConection = oSelect[0]
        nIdGame = oSelect[1]
        oConection.close()

        oData = OperationDB('SEL', 'DISCORD_USER', ['IDMEMBER','USERDESC'], None, "IDMEMBER = '" + cMemberId + "' and IDGAME = " + str(nIdGame), None)
        
        for OneRow in oData:            
            nIdMember = OneRow[0]#IdGame    
            cUserDesc = OneRow[1]#UserDesc

        oData.close()
        return [oData, nIdMember, cUserDesc]

    def ValidateRoleCommand(Self, cCommand: str, cRoleCode: str):
        cStatus = ''
        
        oData = OperationDB('SEL', 'BOT_ROLE', ["'Y' VALIDATE"], None, "ROLEID = (SELECT ROLEID FROM HELPER_ROLE WHERE HELPERCODE = '" + cRoleCode + "') AND BOT_COMMAND = '"+ cCommand +"'", None)        
        
        for OneRow in oData:            
            cStatus = str(OneRow[0])#Validate
        
        print('status: ' + cStatus)

        oData.close()
        if cStatus == 'Y':
            return True
        elif len(cStatus) <= 0:
            return False
                           

    async def GRoleUser(Self, ctx, cIdMember: str, cRoleCode: str):    
        print('application_id: ' + str(bot.application_id))
        MyRoleCommand = []
    
        oConection = None
        oSelect = []
        oSelect = Self.Get_Game_OK()#find a active game
        oConection = oSelect[0]
        nIdGame = oSelect[1]
        oConection.close() 
      
        
        #nIdGame = 13
        #bValidate = foo.Validate_User(cIdMember, nIdGame)#Validate if the user is into the game

        #if bValidate == False:
        #    await ctx.send("User is not in the game, check out!")
        #    return
      
        #cRoleCodeUp = cRoleCode.upper()
        
        #oData = None
        oSelect = []

        #oData = Self.GetRoleCode(bot.application_id, cRoleCodeUp)#Look up the Role Id permition

        oData = None

        oData = OperationDB('SEL', 'BOT_ROLE', ['ROLEID', 'BOT_COMMAND'], None, "ROLEID = (SELECT ROLEID FROM HELPER_ROLE WHERE HELPERCODE = '"+ 'TK' +"') AND APLICATIONID = '"+ str(bot.application_id) +"'", None)        
        
        dblista = []

        for OneRow in oData:
            #print(OneRow)
            #dblista = [OneRow[0],OneRow[1]]
            dblista.append(list(OneRow))
        
        #print(dblista)

        #print(dblista[0][0], dblista[0][1])


        oData.close()
        
        cAplicationId = bot.application_id

        for i in range(len(dblista)):
            print(dblista[i][0], dblista[i][1])#1st [] -> row / 2nd [] -> column
            nIdRole = dblista[i][0]
            nBotCommand = dblista[i][1]
            #Insert a row of a permit-role for a user selected to use a command
            OperationDB('INS', 'ROLE_USERID', ['ROLEID','APLICATIONID','BOT_COMMAND','IDGAME','IDMEMBER','STATUS'],[str(nIdRole), "'"+ str(cAplicationId) + "'", "'"+ str(nBotCommand) + "'", str(nIdGame), "'"+ cIdMember + "'", "'OK'"], None, None)            

            #cIdMember

            #Insert a row of a permit-role for a user selected to use a command
            #OperationDB('INS', 'ROLE_USERID', ['ROLEID','APLICATIONID','BOT_COMMAND','IDGAME','IDMEMBER','STATUS'],[str(nIdRole), "'"+ str(cAplicationId) + "'", "'"+ str(nBotCommand) + "'", str(nIdGame), "'"+ '0947489734785' + "'", "'OK'"], None, None)  

            #Insert a row of a permit-role for a user selected to use a command
            #OperationDB('INS', 'ROLE_USERID', ['APLICATIONID'],[str('79873454353489')], None, None)                    

        #oConection = oSelect[0]
        #nIdRole = oSelect[1]
        #nBotCommand = oSelect[2]
        
        
        #oConection = oSelect[0]
        #nIdRole = oSelect[1]
        #nIdRole = ''
        #nBotCommand = ''
        cAplicationId = bot.application_id
        '''
        for OneRow in MyRoleCommand:
        #for i in range(len(dblista)):
            #print(OneRow)
            nIdRole = OneRow.RoleId
            nBotCommand = OneRow.BotCommand
            '''
        for i in range(len(MyRoleCommand)):
        #for i in range(len(dblista)):
            #print(OneRow)
            nIdRole = MyRoleCommand[i].RoleId
            nBotCommand = MyRoleCommand[i].BotCommand            
            #nIdRole = OneRow[0]
            #nBotCommand = OneRow[1]
            print('nIdRole: ' + str(nIdRole) + ' nBotCommand: ' + str(nBotCommand))
            #Insert a row of a permit-role for a user selected to use a command
            #OperationDB('INS', 'ROLE_USERID', ['ROLEID','APLICATIONID','BOT_COMMAND','IDGAME','IDMEMBER','STATUS'],[str(nIdRole), "'"+ str(cAplicationId) + "'", "'"+ str(nBotCommand) + "'", str(nIdGame), "'"+ cIdMember + "'", "'OK'"], None, None)
            
            #Insert into ROLE_USERID(ROLEID,APLICATIONID,BOT_COMMAND,IDGAME,IDMEMBER,STATUS) values (2,'1071451684691263538','start',13,'705234368758808660','OK')

            #OperationDB('INS', 'DISCORD_USER', ['IDMEMBER','IDGAME','IDCHANNEL','USERDESC','DATEREG','HELPER','PLAYER','STATUS'], ["'" + str(MyMember[i].MemberId) + "'" , str(nIdGame) , "'" + str(cIdChannel) + "'", "'" + str(MyMember[i].MemberName) + "'" , "'" + Self.Get_Time() + "'" , "'N'", "'Y'", "'OK'"], None, None)

            #oConection.commit()
        

    def Get_Point_Rule(Self, cPointCode: str) -> list:
        nIdGame = []
        #look up for a point rule
        oData = OperationDB('SEL', 'POINT_RULE', ['IDPOINT'], None, "POINTCODE = '" + str(cPointCode) + "'", None)        
        
        for OneRow in oData:            
            nIdGame = OneRow[0]#IdGame
        return [oData, nIdGame]        
    
    def GetChannelId(Self, cChannelName: str) -> str:
        cChannel = ''
        for i in range(len(Self.MyChannel)):
            if cChannelName == str(Self.MyChannel[i].ChannelName):
                cChannel = Self.MyChannel[i].ChannelId
                return cChannel
            #print('Class myChannel -> Channel Id: ' + str(foo.MyChannel[i].ChannelId) + ' Name: ' + str(foo.MyChannel[i].ChannelName)) 
    
    def Validate_User(Self, cIdMember: str, nIdGame: int) -> bool:#Validate if the user is into the Voice Channel
        nIdMember = ''
        oData = OperationDB('SEL', 'DISCORD_USER', ['IDGAME','IDMEMBER'], None, "STATUS = 'OK' AND IDGAME = " + str(nIdGame) + " AND IDMEMBER = '" + cIdMember + "'", None)        

        for OneRow in oData:            
            #nIdGame = OneRow[0]#IdGame
            nIdMember = str(OneRow[1])#IdMember
        oData.close()
        if len(nIdMember) <= 0:
            return False
        elif len(nIdMember) > 0:
            return True

    @commands.Cog.listener()
    async def ShowScoreCard(Self, ctx):
        MyScore = []
  
        cUserDesc = []
        oData = None
        oConection = None
        
        #look up for a point rule
        oData = OperationDB('SEL', 'SCORECARD', ['IDMEMBER','SUM(POINT) POINT'], None, "IDMEMBER IN(SELECT IDMEMBER FROM DISCORD_USER WHERE STATUS = 'OK') AND IDGAME IN(SELECT IDGAME FROM GAME WHERE STATUS = 'OK')", ' GROUP BY IDMEMBER ORDER BY 2 DESC')        
        
        for OneRow in oData:
            print(OneRow[0],OneRow[1])

            oSelect = []
            oSelect = Self.Get_MemberId(str(OneRow[0]))#find a member from DISCORD_USER's table                        
            oConection = oSelect[0]
            cUserDesc = oSelect[2]
            oConection.close()

            MyScore.append(Self.ScoreCardDetail(OneRow[0], cUserDesc, OneRow[1]))

        if MyScore is None:
            await ctx.send('ScoreCard empty!')
            return

        embed = discord.Embed(title='', description="The Three Questions' Game", color=discord.Color.blue())
        
        embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvlJsqbDBYjobCSePQghhuHn6Ph5eDhQql6Q&usqp=CAU")

        for Row in MyScore:
            #print(Row.IdMember, Row.UserDesc, Row.nPointTotal)
            embed.add_field(name=str(Row.UserDesc) + ':', value=f"{str(Row.nPointTotal)}")

        oData.close()
        await ctx.send(embed=embed)        

    @commands.Cog.listener()
    async def info(Self, ctx):
        MyScore = []
        
        #MyScore = Self.ShowScoreCard()        

        #oConection = oSelect[0]
        #nIdMember = oSelect[1]
        #cUserDesc = oSelect[2]
        #oConection.close()         
        if MyScore is None:
            await ctx.send('ScoreCard empty!')
            return

        embed = discord.Embed(title=f"{ctx.guild.name}", description="The Three Questions' Game", timestamp=datetime.utcnow(), color=discord.Color.blue())

        embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvlJsqbDBYjobCSePQghhuHn6Ph5eDhQql6Q&usqp=CAU")

        #rows = oSelect.fetchall() 
        #for row in oSelect:
            #print(row)
        print('---------------------------------')
        print(range(len(MyScore)))

        #for i in range(len(MyScore)):
        nCont = 0
        for Row in MyScore:
            while nCont in range(len(MyScore)):
                print(nCont, Row[nCont].IdMember, Row[nCont].UserDesc, Row[nCont].nPointTotal)
                #print(nCont, Row[1].IdMember, Row[1].UserDesc, Row[1].nPointTotal)
                nCont += 1
        
        print('total objetos: '+ str(len(MyScore)))

        for Row in MyScore:
            for i in range(len(MyScore)):
                print(i, Row[i].IdMember, Row[i].UserDesc, Row[i].nPointTotal)
                embed.add_field(name=str(Row[i].UserDesc) + ':', value=f"{str(Row[i].nPointTotal)}")

        #for i in range(len(MyScore)):
        #    print(MyScore[i].IdMember, MyScore[i].UserDesc, MyScore[i].nPointTotal)
            #print(Row.IdMember, Row.UserDesc, Row.nPointTotal)            

        #oConection.close()
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def strtgame(Self, ctx):
        """
        Start the Three Questions' Game

        Example: !startgame
        """
        #member = ctx.author
        print('start game')
        #cIdChannel = '1072469507504873492'
        
        MyChannel = Self.MyChannel
        cIdChannel = MyChannel[0].ChannelId        
        #channel = bot.get_channel(1071493291876552872)

        print('guild: ' + str(ctx.guild.id) + ' author: ' , ctx.author)
        #'Channel: ' + str(ctx.channel.id)
        oData = OperationDB('SEL', 'GAME', ['IDGAME'], None, "STATUS = 'OK' and IDCHANNEL = '" + cIdChannel + "'", None)
        '''
        for row in oData:
            #print(row[0] , row[1], row[2])        
            print(row)'''
        #print(len(oData.fetchall()))
        print('Total of rows: ' + str(len(oData.fetchall())))
        
        if len(oData.fetchall()) <= 0:#verifying if the table is empty
            print('Tabla vacia')
            now = datetime.now()        
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            
            #Insert a row of a game of a Channel Room
            OperationDB('INS', 'GAME', ['IDCHANNEL','DATESTARTGAME','DESCRIPTION','STATUS'], ["'"+ cIdChannel + "'", "'"+ current_time + "'", "'TQD game'", "'OK'"], '', None)
        else:#show a meesage in Discord
            await ctx.send('Game have been started, to stop the game type: !stopgame')
        oData.close()
        
        await foo.PostGeneralInfo(ctx, 'GAME STARTED', "The Three Questions' Game",["⦁	challenges us to do fun and interesting verbal Presentations in Spanish or English! After each Presentation we do a Follow-Up Question Round when everybody gets to ask a nice follow-up question related to the Presentation.", "⦁	We 'conquer our nerves' by practicing a smooth, confident and professional style of delivery.","⦁	We try to keep the microphone clear for the Player and Co-Host. However, we are all free to discuss things in the Text Chat. We also like to type out nice compliments and cool vocabulary to help people feel good about themselves and improve!","⦁	You'll be asking Follow-Up Questions and eventually, you will be asked to do a brief Presentation. Take some notes before your Presentation if you can. Gracias!"])

        await Self.allmembers(ctx)#list all members of Channel Room
    
    @commands.Cog.listener()
    async def stpgame(Self, ctx):
        """
        Stop the Three Questions' Game

        Example: !stopgame
        """        
        
        await foo.ShowScoreCard(ctx)#show final scorecard        
        
        oSelect = []
        oSelect = foo.Get_Game_OK()#find a active game
        oConection = oSelect[0]
        nIdGame = oSelect[1]
        oConection.close()

        #update the state's user in the table DISCORD_USER to OUT
        OperationDB('UPD', 'GAME', "STATUS = 'END'", None, "IDGAME = " + str(nIdGame), None)
        
        #kick out all member from the game by the status: OK -> OUT
        OperationDB('UPD', 'DISCORD_USER', "STATUS = 'OUT'", None, "IDGAME = " + str(nIdGame), None)

        await foo.PostGeneralInfo(ctx, 'GAME OVER', "The Three Questions' Game",["Game over, thanks for participating!", "Juego finalizado, gracias por participar!"])

    @commands.Cog.listener()
    async def allmembers(Self, ctx):#, member : discord.member
        MyChannel = Self.MyChannel
        cIdChannel = str(MyChannel[0].ChannelId)

        print('cIdChannel: ' + cIdChannel)

        MyMember = []
        channel = bot.get_channel(int(cIdChannel))               

        members = channel.members
        
        print(channel)
        print(members)
        print('all members')

        oData = OperationDB('SEL', 'GAME', ['IDGAME'], None, "STATUS = 'OK' and IDCHANNEL = '" + str(cIdChannel) + "'", None)        
        
        for OneRow in oData:
            nIdGame = OneRow[0]#IdGame

        print('IdGame: ' + str(nIdGame))
        
        oData.close()

        MyMember = []
        
        for member in members:
            MyMember.append(Self.MemberDetail(member.id, member.name, channel.id))

        for i in range(len(MyMember)):
            print('Channel Id: ' + str(MyMember[i].ChannelRoomId) + ' id: ' + str(MyMember[i].MemberId) + ' User: ' + str(MyMember[i].MemberName))
            
            '''
            oSelect = []
            oSelect = Self.Get_MemberId(str(MyMember[i].MemberId))#Find is a member exists in the table: DISCORD_USER
            nMemberId = oSelect[0]
            oConection = oSelect[0]
            '''
            
            #if len(nMemberId) == 0:
            #Insert a row of a game of a Channel Room
            OperationDB('INS', 'DISCORD_USER', ['IDMEMBER','IDGAME','IDCHANNEL','USERDESC','DATEREG','HELPER','PLAYER','STATUS'], ["'" + str(MyMember[i].MemberId) + "'" , str(nIdGame) , "'" + str(cIdChannel) + "'", "'" + str(MyMember[i].MemberName) + "'" , "'" + Self.Get_Time() + "'" , "'N'", "'Y'", "'OK'"], None, None)

            #oConection.close()

    @commands.Cog.listener()
    async def SavePoint(Self, ctx, cPointCode: str, cMemberId: str, nPoint: int, cSource: str):

        oSelect = []
        oSelect = foo.Get_Game_OK()#find a active game
        
        
        oConection = oSelect[0]
        nIdGame = oSelect[1]
        oConection.close()    

        oSelect = []
        oSelect = foo.Get_Point_Rule(cPointCode.upper())#find a point rule
        
        oConection = oSelect[0]
        nIdPoint = oSelect[1]
        

        if oSelect is None:
            ctx.send('Point Rule parameter is incorrect')
            return

        oConection.close()    
        

        cMemberIdClean = cMemberId

        cMemberIdClean = cMemberIdClean.replace('@','')
        cMemberIdClean = cMemberIdClean.replace('<','')
        cMemberIdClean = cMemberIdClean.replace('>','')
        print('member id: '+ cMemberIdClean)

        nIdMember = []

        oData = OperationDB('SEL', 'DISCORD_USER', ['IDGAME','IDMEMBER'], None, "STATUS = 'OK' AND IDGAME = " + str(nIdGame) + " AND IDMEMBER = '" + cMemberIdClean + "'", None)        

        for OneRow in oData:            
            nIdGame = OneRow[0]#IdGame
            nIdMember = OneRow[1]#IdMember

        if len(nIdMember) > 0:
            #Insert a member into the game
            OperationDB('INS', 'SCORECARD', ['IDGAME','IDPOINT','IDMEMBER','DIS_IDGAME','POINT','DATEREG'], [str(nIdGame), str(nIdPoint), "'" + str(nIdMember) + "'", str(nIdGame), str(nPoint), "'" + foo.Get_Time() + "'"], None, None)
            
            
            if cSource == None:
                await Self.ShowScoreCard(ctx)#show ScoreCard

        elif len(nIdMember) <= 0:
            await ctx.send("User is not in the game, check out!")

        oData.close()
        #return [nIdGame, oData]    

#def setup(bot):#register the Cog
#    bot.add_cog(Events(bot))  

@bot.event
async def on_ready():
    print('on_ready')
    print('We have logged in as {}'.format(bot.user))

@bot.event
async def on_voice_state_update(member:discord.Member, before, after): 
    #Global: cMemberId

    bStatus = False
    
    bStatus = foo.Get_GameStatus()
    #print('bStatus: ' + str(bStatus))
    if bStatus == False:#find a active game
        return


    cMemberId = member.id

    if member == bot.user:  #CATCH
        return
    
    if str(after.channel) == 'Lounge':
        print('channel: ' + str(before.channel) + ' - ' + str(after.channel) + ' Id Channel: ' + str(foo.GetChannelId(str(after.channel))))
        #print('mute: ' + str(after.Self_mute))

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
        
        oConection = oSelect[0]
        nIdGame = oSelect[1]        
        oConection.close()

        print('event before oConection.rowcount: ' + str(oConection.rowcount))
        
        oSelect = []
        oSelect = foo.Get_MemberId(str(member.id))#find a member from DISCORD_USER's table        
        oConection = oSelect[0]        
        nIdMember = oSelect[1]

        if len(nIdMember) > 0:

            #update the state's user in the table DISCORD_USER to OUT
            OperationDB('UPD', 'DISCORD_USER', "STATUS = 'OUT'", None, "IDMEMBER = '" + str(member.id) + "' and IDGAME = " + str(nIdGame), None)             
        
        oConection.close()
       
        return

    elif after.channel is not None: #User has joined a voice channel
        
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
                oConection = oSelect[0]
                nIdGame = oSelect[1]
                
                oConection.close()

                oSelect = []
                oSelect = foo.Get_MemberId(str(member.id))
                oConection = oSelect[0]
                nIdMember = oSelect[1]
                

                print('member id from select: ' + str(nIdMember))
                print('total rows from select: ' + str(len(nIdMember)))
                
                #if oData.rowcount() > 0:
                if len(nIdMember) > 0:

                    #update the state's user in the table DISCORD_USER to OK
                    OperationDB('UPD', 'DISCORD_USER', "STATUS = 'OK'", None, "IDMEMBER = '" + str(member.id) + "' and IDGAME = " + str(nIdGame), None)                          
                    print('Member in DISCORD_USER: ' + nIdMember)

                elif len(nIdMember) <= 0:
                    
                    cIdChannel = str(foo.GetChannelId(str(after.channel)))#find the ChannelId

                    #Insert a member into the game
                    OperationDB('INS', 'DISCORD_USER', ['IDMEMBER','IDGAME','IDCHANNEL','USERDESC','DATEREG','HELPER','PLAYER','STATUS'], ["'" + str(member.id) + "'" , str(nIdGame) , "'" + str(cIdChannel) + "'", "'" + str(member.name) + "'" , "'" + foo.Get_Time() + "'" , "'N'", "'Y'", "'OK'"], None, None)

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

foo = OperDiscord(commands.Cog)#Instans a class

@bot.command()
async def helpgame(ctx, cCommand: str):
    #if cCommand == '*':
        #pass
    if cCommand == 'helpgame' or cCommand == '*':
        await foo.PostGeneralInfo(ctx, 'Command: !helpgame', 'Parameters: * command',["Example: !helpgame","Show information about all allowed commands for the game"])
    if cCommand == 'startgame' or cCommand == '*':
        await foo.PostGeneralInfo(ctx, 'Command: !startgame', 'Parameters: None',["Example: !startgame", "Start the Three Questions' Game"])
    if cCommand == 'stopgame' or cCommand == '*':
        await foo.PostGeneralInfo(ctx, 'Command: !stopgame', 'Parameters: None',["Example: !stopgame","Stop the Three Questions' Game"])
    if cCommand == 'savescore' or cCommand == '*':
        await foo.PostGeneralInfo(ctx, 'Command: !savescore', 'Parameters: Point_code @User Score',["Example: !savescore P @user score", "Registry the score of a player and depends of the parameter Point Code",'Reference: * Point_code -> (ej. P = Presentation / Q = Follow-Question)','@User -> User member inside the voice room','Score -> Score won'])
        #savescore(ctx, cPointCode: str, cMemberId: str, nPoint: int):
    if cCommand == 'gamestatus' or cCommand == '*':
        await foo.PostGeneralInfo(ctx, 'Command: !gamestatus', 'Parameters: None',["Example: !gamestatus","Show the status of the current game: Active / Inactive"])
    if cCommand == 'infogame' or cCommand == '*':
        await foo.PostGeneralInfo(ctx, 'Command: !infogame', 'Parameters: None',["Example: !infogame","Show the scorecard of the current game of all the players that are inside the room"])
    if cCommand == 'start' or cCommand == '*':
        await foo.PostGeneralInfo(ctx, 'Command: !start', 'Parameters: Role_game @User',["Example: !start P @user01","Manage and start the timer of Presentation or Follow-Question",'Reference: * Role_game -> (ej. P = Presentation / Q = Follow-Question)','@User -> User member inside the voice room'])
    if cCommand == 'stop' or cCommand == '*':
        await foo.PostGeneralInfo(ctx, 'Command: !stop', 'Parameters: None',["Example: !stop","stop the timer of Presentation or Follow-Question","Presentations or Follow-Questions can win score bonuses"])    

@bot.command()
async def startgame(ctx):
    """
    Start the Three Questions' Game

    Command: !startgame

    Description: Start the Three Questions' Game
    """
    bStatus = False

    bStatus = foo.Get_GameStatus()
    #print('bStatus: ' + str(bStatus))
    if bStatus:#find a active game
        await foo.PostGeneralInfo(ctx, 'WARNING', 'Exists a game started',["To start a new game, first you need close the current game with: !stopgame"])
        return

    await foo.strtgame(ctx)

@bot.command()
async def stopgame(ctx):
    """
    Stop the Three Questions' Game

    Example: !stopgame
    """

    bStatus = False
    
    bStatus = foo.Get_GameStatus()
    #print('bStatus: ' + str(bStatus))
    if bStatus == False:#find a active game
        await foo.PostGeneralInfo(ctx, 'WARNING', "Doesn't exists a game started",["To close a current game, first you need start a new game with: !startgame"])
        return

    await foo.stpgame(ctx)

@bot.command()
async def gamestatus(ctx):
    """
    Command: !gamestatus
    Parameters: None
    Description: show the status of the game (Active / Inactive)
    """

    bStatus = foo.Get_GameStatus()
    print('bStatus: ' + str(bStatus))
    if bStatus:#find a active game
        embed = discord.Embed(title='', description="The Three Questions' Game", color=discord.Color.blue())

        embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvlJsqbDBYjobCSePQghhuHn6Ph5eDhQql6Q&usqp=CAU")

    
        embed.add_field(name='Game active and started' + ':', value="")

        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='', description="The Three Questions' Game", color=discord.Color.red())

        embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvlJsqbDBYjobCSePQghhuHn6Ph5eDhQql6Q&usqp=CAU")

    
        embed.add_field(name='Game INACTIVE' + ':', value="")       

        await ctx.send(embed=embed) 
    

@bot.command()#Regitry a score
async def savescore(ctx, cPointCode: str, cMemberId: str, nPoint: int):

    bStatus = False
    
    bStatus = foo.Get_GameStatus()
    #print('bStatus: ' + str(bStatus))
    if bStatus == False:#find a active game
        await foo.PostGeneralInfo(ctx, 'WARNING', "Doesn't exists a game started",["You need start a new game with: !startgame"])
        return

    await foo.SavePoint(ctx, cPointCode, cMemberId, nPoint, None)

@bot.command()
async def infogame(ctx):#Post scorecard

    bStatus = False
    
    bStatus = foo.Get_GameStatus()
    #print('bStatus: ' + str(bStatus))
    if bStatus == False:#find a active game
        await foo.PostGeneralInfo(ctx, 'WARNING', "Doesn't exists a game started",["You need start a new game with: !startgame"])
        return

    await foo.ShowScoreCard(ctx)

cMemberGlobal = ''
cProcedureGlobal = ''

@bot.command()
async def start(ctx, cProcedure: str, cUser: str):#start timer
    global cMemberGlobal
    global cProcedureGlobal

    bStatus = False
    
    bStatus = foo.Get_GameStatus()
    #print('bStatus: ' + str(bStatus))
    if bStatus == False:#find a active game
        await foo.PostGeneralInfo(ctx, 'WARNING', "Doesn't exists a game started",["You need start a new game with: !startgame"])
        return    

    cMemberGlobal = cUser
    cProcedureGlobal = cProcedure

    oSelect = []
    oSelect = foo.Get_Game_OK()#find a active game
    oConection = oSelect[0]
    nIdGame = oSelect[1]
    oConection.close()    

    cMemberGlobal = cMemberGlobal.replace('@','')
    cMemberGlobal = cMemberGlobal.replace('<','')
    cMemberGlobal = cMemberGlobal.replace('>','')    

    bValidate = foo.Validate_User(cMemberGlobal, nIdGame)

    if bValidate:
        pass
    else:
        await ctx.send("User is not in the game, check out!")
        return

    await starttimer(ctx, cProcedure, cUser)
    

@bot.command()
async def stop(ctx):#Sop Timer
    global cMemberGlobal
    global cProcedureGlobal

    bStatus = False
    
    bStatus = foo.Get_GameStatus()
    #print('bStatus: ' + str(bStatus))
    if bStatus == False:#find a active game
        await foo.PostGeneralInfo(ctx, 'WARNING', "Doesn't exists a game started",["You need start a new game with: !startgame"])
        return

    #cMember = member:discord.Member
    LastTime = await stoptimer(ctx)
    
    print('LastTime: ' + str(LastTime))
    print('cProcedureGloba: ' + cProcedureGlobal)    
    if 30 <= LastTime <= 75 and cProcedureGlobal.upper() == 'P':
        cMemberGlobal = cMemberGlobal.replace('@','')
        cMemberGlobal = cMemberGlobal.replace('<','')
        cMemberGlobal = cMemberGlobal.replace('>','')
        #print('member stop method: ' + str(cMemberGlobal))
        
        await foo.SavePoint(ctx, 'R', cMemberGlobal, 3, 'stop')#Registry a Bonus Point

        embed = discord.Embed(title='', description="The Three Questions' Game", color=discord.Color.blue())

        embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvlJsqbDBYjobCSePQghhuHn6Ph5eDhQql6Q&usqp=CAU")

    
        embed.add_field(name='BONUS Point by Presentation' + ':', value="+3 for Presentations that finish between 30 to 75 seconds")

        await ctx.send(embed=embed)

        await foo.ShowScoreCard(ctx)
    
    if 15 <= LastTime <= 40 and cProcedureGlobal.upper() == 'Q':
        cMemberGlobal = cMemberGlobal.replace('@','')
        cMemberGlobal = cMemberGlobal.replace('<','')
        cMemberGlobal = cMemberGlobal.replace('>','')
        #print('member stop method: ' + str(cMemberGlobal))

        await foo.SavePoint(ctx, 'R', cMemberGlobal, 1, 'stop')#Registry a Bonus Point

        embed = discord.Embed(title='', description="The Three Questions' Game", color=discord.Color.blue())

        embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvlJsqbDBYjobCSePQghhuHn6Ph5eDhQql6Q&usqp=CAU")

    
        embed.add_field(name='BONUS Point by Follow-Question' + ':', value="+1 For each Follow-Up Response between 15 - 40 seconds")

        await ctx.send(embed=embed)

        await foo.ShowScoreCard(ctx)

@bot.command()#Give permission's commands to an user
async def giverole(ctx, cIdMember: str, cRoleCode: str):

    #bStatus = False
    
    #bStatus = foo.Get_GameStatus()#if not exists a OK's game, then show a warning's message and cannot continues

    #print('bStatus: ' + str(bStatus))
    #if bStatus == False:#find a active game
    #    await foo.PostGeneralInfo(ctx, 'WARNING', "Doesn't exists a game started",["You need start a new game with: !startgame"])
    #    return

    cMemberLocal = cIdMember
    cMemberLocal = cMemberLocal.replace('@','')
    cMemberLocal = cMemberLocal.replace('<','')
    cMemberLocal = cMemberLocal.replace('>','')   
    
    #OperationDB('INS', 'TIMER_RULE', ['STATUS'],["'OK'"], None, None)
    #OperationDB('INS', 'ROLE_USERID', ['STATUS'],[ "'OK'"], None, None)                    

    #OperationDB('INS', 'TIMER_RULE', ['STATUS'], ["'OK'"], None, None)

    await foo.GRoleUser(ctx,cMemberLocal, cRoleCode)

@bot.command()#Revoke permission's commands to an user
async def removerole(ctx, cIdMember: str, cCommand: str, cRoleCode: str):
    bStatus = False
    
    bStatus = foo.Get_GameStatus()#if not exists a OK's game, then show a warning's message and cannot continues
    
    #print('bStatus: ' + str(bStatus))
    if bStatus == False:#find a active game
        await foo.PostGeneralInfo(ctx, 'WARNING', "Doesn't exists a game started",["You need start a new game with: !startgame"])
        return

    #await foo.GRoleUser(ctx,cIdMember, cCommand, cRoleCode)

@bot.command()#Revoke permission's commands to an user
async def clonerole(ctx, cIdMember: str, cCommand: str):
    bStatus = False
    
    bStatus = foo.Get_GameStatus()#if not exists a OK's game, then show a warning's message and cannot continues
    
    #print('bStatus: ' + str(bStatus))
    if bStatus == False:#find a active game
        await foo.PostGeneralInfo(ctx, 'WARNING', "Doesn't exists a game started",["You need start a new game with: !startgame"])
        return

    #await foo.GRoleUser(ctx,cIdMember, cCommand)

bot.run(format(env['BOT_TOKEN']))#Start the Bot