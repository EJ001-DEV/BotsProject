import asyncio
import discord
import sqlite3
import os
from datetime import datetime
from timer import Timer, TimerStatus
from discord.ext import commands

from os import environ as env

from dotenv import load_dotenv

COLOR_DANGER = 0xc63333
COLOR_SUCCESS = 0x33c633

class DiscordCog(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.timer = Timer()
        self.db = sqlite3.connect('db_TQG.db')
        self.create_tables()
        print('init')


    def create_tables(self):
        print('create table')
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


    @commands.command
    def init_bot(self):
        intents = discord.Intents.all()
        intents.message_content = True

        self.bot = commands.Bot(command_prefix='!', description="This is a helper bot",intents= intents)

               


    @commands.Cog.listener()
    async def on_ready(self):
        print('on_ready')
        print('We have logged in as {}'.format(self.bot.user))

    @commands.command()
    async def table(self):
        await self.create_tables()

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
    

load_dotenv()

oOper = DiscordCog(commands)

#with DiscordCog() as db:
#    db.create_tables()
    
#DiscordCog.create_tables(self=)
    
#DiscordCog.init_bot()
    #print('BOT_TOKEN:  {}'.format(env['BOT_TOKEN']))
    #run(format(env['BOT_TOKEN'])) 
    