import asyncio
import discord
import sqlite3
import os
from datetime import datetime
from timer import Timer, TimerStatus
from dotenv import load_dotenv
from discord.ext import commands

COLOR_DANGER = 0xc63333
COLOR_SUCCESS = 0x33c633



class DiscordCog(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.timer = Timer()
        self.db = sqlite3.connect('main.db')
        self.create_tables()


    def create_tables(self):
        cur = self.db.cursor()
        # Create table
        cur.execute('''
        CREATE TABLE IF NOT EXISTS alarms (
            id integer PRIMARY KEY AUTOINCREMENT,
            username text NOT NULL,
            start_time text NOT NULL,
            delay text NOT NULL
            )
        ''')
        self.db.commit()


    @commands.Cog.listener()
    async def on_ready(self):
        print('We have logged in as {}'.format(self.bot.user))


    @commands.command()
    async def start(self, ctx):
        if self.timer.get_status() == TimerStatus.RUNNING:
            await self.show_message(ctx, "Timer is already running! You should stop the timer before you can restart it!", COLOR_SUCCESS)    
            return

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        cur = self.db.cursor()
        cur.execute('''
        INSERT INTO alarms (username, start_time, delay)
            VALUES (?,?,?)
        ''', [str(ctx.author),current_time,'10'])
        self.db.commit()

        cur = self.db.cursor()
        for row in cur.execute('SELECT * FROM alarms'):
            print(row)

        await self.show_message(ctx, "Time to start working!", COLOR_SUCCESS)
        self.timer.start(max_ticks=10)
        while self.timer.get_status() == TimerStatus.RUNNING:
            await asyncio.sleep(1)
            self.timer.tick()
        if self.timer.get_status() == TimerStatus.EXPIRED:
            await self.show_message(ctx, "Time to start your break!", COLOR_SUCCESS)
            self.timer.start(max_ticks=10)
            while self.timer.get_status() == TimerStatus.RUNNING:
                await asyncio.sleep(1)
                self.timer.tick()
            if self.timer.get_status() == TimerStatus.EXPIRED:
                await self.show_message(ctx, "Okay, break over!", COLOR_SUCCESS)


    async def show_message(self, ctx, title, color):
        start_work_em = discord.Embed(title=title, color=color)
        await ctx.send(embed=start_work_em)


    @commands.command()
    async def stop(self, ctx):
        if self.timer.get_status() != TimerStatus.RUNNING:
            await self.show_message(ctx, "Timer is already stopped! You should start the timer before you can stop it!", COLOR_SUCCESS)    
            return        
        await self.show_message(ctx, "Timer has been stopped!", COLOR_DANGER)
        self.timer.stop()


    @commands.command()
    async def show_time(self, ctx):
        await ctx.send(f"Current timer status is : {self.timer.get_status()}")
        await ctx.send(f"Current time is : {self.timer.get_ticks()}")


    @commands.command()
    async def show_help(self, ctx):
        help_commands = dict()
        for command in self.bot.commands:
            help_commands[command.name] = command.help
        description = "Bot commands are: {}".format(help_commands)
        show_help_em = discord.Embed(title="This is Mr Pomo Dorio, a friendly Pomodoro bot", description=description,
                                    color=COLOR_SUCCESS)
        await ctx.send(embed=show_help_em)

#DiscordCog.create_tables()
load_dotenv()

def setup(bot):
    bot.add_cog(DiscordCog(bot))
    print("Scrims cog is loaded!")

'''
async def main():
    """
    Create the tables and columns if they don't already exist,
     If using sqlite, it'll create the .db file as well
    """
    async with engine.begin() as conn:
            # drop all tables, if any exists  
            # await conn.run_sync(Base.metadata.drop_all)
            # actually create any non existing tables and columns inside the database
        await conn.run_sync(Base.metadata.create_all)

        # close and clear open connection pools
        await engine.dispose()



if __name__ == "__main__":
    # use asyncio to run the create_tables function
    import asyncio

    asyncio.run(main())
'''