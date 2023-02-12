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


class OperDiscord(commands.Cog):

    class MemberDetail():
        def __init__(self, MemberId, MemberName, ChannelRoomId):
            self.MemberId = MemberId
            self.MemberName = MemberName
            self.ChannelRoomId = ChannelRoomId

    def __init__(self, bot):
        self.bot = bot    
        intents = discord.Intents.all()
        intents.message_content = True
        intents.members = True

        self.bot = commands.Bot(command_prefix='!', description="This is a helper bot",intents= intents)        

    @commands.Cog.listener()
    async def on_ready(self):
        print('on_ready')
        print('We have logged in as {}'.format(self.bot.user))
        await self.bot.change_presence(activity=discord.Streaming(name="Three Questions' Game",url=""))

    @commands.Cog.listener()
    async def startgame(self, ctx):
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
        MyMember = []
        #MyMember.append(self.MemberDetail(705234368758808660, 'EJ001',1072469507504873492))
        #MyMember.append(self.MemberDetail(1071451684691263538, 'TQGBot',1072469507504873492))
        #MyMember.append(self.MemberDetail(1071563913243668570, 'BotTest',1072469507504873492))
        #ej = self.MemberDetail(705234368758808660, 'EJ001',1072469507504873492)
        #tqg = self.MemberDetail(1071451684691263538, 'TQGBot',1072469507504873492)
        #test = self.MemberDetail(1071563913243668570, 'BotTest',1072469507504873492)
        #MyMember = [ej, tqg, test]
        #print('id: ' + str(MyMember[0].MemberId) + ' User: ' + str(MyMember[0].MemberName))
        #print('id: ' + str(MyMember[2].MemberId) + ' User: ' + str(MyMember[2].MemberName))
        
        channel = self.bot.get_channel(1072469507504873492) 

        members = channel.members

        print(channel)
        print(members)

        MyMember = []
        
        for member in members:
            MyMember.append(self.MemberDetail(member.id, member.name,channel.id))


        #print(memids, memstatus, memname) #print info
        #print('id: ' + str(MyMember[0].MemberId) + ' User: ' + str(MyMember[0].MemberName))

        for i in range(len(MyMember)):
            print('Channel Id: ' + str(MyMember[i].ChannelRoomId) + ' id: ' + str(MyMember[i].MemberId) + ' User: ' + str(MyMember[i].MemberName))

        '''
        for member in self.bot.get_all_members():
            #print(ctx.guild.channels, member.guild.get_channel('1072469507504873492'))        
            
            channel = ctx.message.author.voice.channel
            members = channel.members
            for utente in members:
                await utente

            print(members)
            print(member)     
        '''   
            #print(member.guild.get_channel(1072469507504873492), member )        
            #print(member.guild.get_channel(1072469507504873492), member._get_channel)
            #member.guild.channels
            
            #print(member.guild.get_channel(1072469507504873492))
            #print(member, self.bot.get_all_members())
        

        '''
        #cIdChannel = '1072469507504873492'    
        channel = self.bot.get_channel('1072469507504873492') #gets the channel you want to get the list from
        #channel.members.count
        
        members = channel.members #finds members connected to the channel
        #members.
        memids = [] #(list)
        for member in members:
            memids.append(member.id)

        print(memids) #print info    
        print(self.bot.get_user(memids[0]))        
        '''        

        #print('Now: ' + str(now) + ' Current_time: ' + current_time)


foo = OperDiscord(commands.Cog)


@foo.bot.command()
async def OperGame(ctx):
    #member = ctx.author
    await foo.allmembers(ctx)#member=discord.member
    await foo.startgame(ctx)


'''
oData = OperationDB('SEL', 'VOICE_CHANNEL', ['IDCHANNEL','CHANNELNAME'], None, "IDCHANNEL = '1071493291876552872'")

for i in oData:
    print(i)
oData.close()
'''

foo.bot.run(format(env['BOT_TOKEN']))

#oOperDB.ProcSelect('channel2', ['id','username','delay'], "username = 'EJ001'")