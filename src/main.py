import discord
import aiosqlite
import asyncio
from discord.ext import tasks, commands

from os import environ as env
from dotenv import load_dotenv

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='>', description="This is a helper bot",intents= intents)

@bot.command()
async def adduser(ctx, member:discord.Member):
    member = ctx.author
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT id FROM users WHERE guild = ?",(ctx.guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("UPDATE users SET id = ? WHERE guild = ?", (member.id, ctx.guild.id))
            else:
                await cursor.execute("INSERT INTO users(id, guild) VALUES(?, ?)", (member.id, ctx.guild.id))
        await db.commit()

@bot.command()
async def removeuser(ctx, member:discord.Member):
    member = ctx.author
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT id FROM users WHERE guild = ?",(ctx.guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("DELETE FROM users WHERE id = ? and guild = ?", (member.id, ctx.guild.id))
            else:
                await ctx.send('User not found')
        await db.commit()        

@bot.command()
async def post_info(ctx):
    #member:discord.Member
    await ctx.send(ctx.author)

@bot.command()
async def allmembers(ctx):
    channel = bot.get_channel(1071493291876552872) #gets the channel you want to get the list from

    members = channel.members #finds members connected to the channel

    memids = [] #(list)
    for member in members:
        memids.append(member.id)

    print(memids) #print info    
    print(bot.get_user(memids[0]))

#Events
@bot.event
async def on_ready():    
    print("My Bot is ready")    
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTERGER, guild INTEGER)")
        await db.commit()
'''
@bot.event
async def on_voice_state_update(member:discord.Member, before, after):
    #if not before.channel and after.channel and member.id == 245276992432373760:
    print(f'{member} has joined the vc')
'''

@bot.event
async def on_voice_state_update(member:discord.Member, before, after):
    if member == bot.user:  #CATCH
        return

    if after.channel is None: #User has left a voice channel
        print(f'{member} User left voice channel')
        #print(f'{member} Joined Channel')
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

load_dotenv()
bot.run(format(env['BOT_TOKEN']))   

