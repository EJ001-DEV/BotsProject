import asyncio
import discord
import sqlite3
import os
from datetime import datetime
from timer import Timer, TimerStatus
from discord.ext import commands

from os import environ as env

from dotenv import load_dotenv

class ScrimsCog(commands.Cog, name='Scrims-Commands') :

        def __init__(self,bot):
            self.bot = bot
    
        @commands.Cog.listener()
        async def on_message(self,message):
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {message.guild.id}")
            result =  cursor.fetchone()
            if result is None:
                return
            else:
                #cursor.execute(f"SELECT role FROM main WHERE guild_id = {message.guild.id}")
                
                cursor.execute("SELECT channel_id FROM main WHERE guild_id = ?", [message.guild.id])
                result =  cursor.fetchone()
                if not discord.TextChannel == result:
                    return
                if len(message.mentions) >= 3:
                    await message.add_reaction(emoji="<a:tick:748476262640779276>")
                role = discord.utils.get(message.guild.roles, name=role)
                user = message.author
                await user.add_roles(role)
            await self.bot.process_commands(message)
            

        
        
        @commands.group(invoke_without_command=True)
        async def scrimsmod(self,ctx):
            await ctx.send('Available Setup Commands: \nscrimsmod channel <#channel>\nscrimsmod role  <message>')
        @scrimsmod.command()
        async def channel(self, ctx, channel:discord.TextChannel):
            if ctx.message.author.guild_permissions.manage_messages:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()
                cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
                result =  cursor.fetchone()
                if result is None:
                    sql = ("INSERT INTO main(guild_id, channel_id) VALUES(?,?)")
                    val = (ctx.guild.id, channel.id)
                    await ctx.send(f" Default Registration Channel has been set to {channel.mention}")
                elif result is not None:
                    sql = ("UPDATE main SET channel_id = ? WHERE guild_id = ?")
                    val = (channel.id, ctx.guild.id)
                    await ctx.send(f"Default Registration Channel has been updated to {channel.mention}")
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

        @scrimsmod.command()
        async def role(self, ctx,role: discord.Role):
            if ctx.message.author.guild_permissions.manage_messages:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()
                cursor.execute(f"SELECT role FROM main WHERE guild_id = {ctx.guild.id}")
                result =  cursor.fetchone()
                if result is None:
                    sql = ("INSERT INTO main(guild_id, role) VALUES(?,?)")
                    val = (ctx.guild.id, role)
                    await ctx.send(f"Default role to give on correct registration have been set to `{role}`")
                elif result is not None:
                    sql = ("UPDATE main SET role = ? WHERE guild_id = ?")
                    val = (role, ctx.guild.id)
                    await ctx.send(f"Default role to give on correct registration have been updated to  `{role}`")
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
    

def setup(bot):
    print("Scrims cog is loaded!")
    bot.add_cog(ScrimsCog(bot))
    
'''
async def main(bot):    
    bot.add_cog(ScrimsCog(bot))
    print("Scrims cog is loaded!")
'''
if __name__ == "setup1":
    # use asyncio to run the create_tables function
    import asyncio

    asyncio.run(setup())

#foo = ScrimsCog(ctx, commands,'')
#foo.on_message()