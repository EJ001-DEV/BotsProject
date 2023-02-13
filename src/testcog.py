import discord
from discord.ext import commands, tasks
#################################
#Both library to gets values from .env file
from dotenv import load_dotenv
from os import environ as env
#################################
import os
import datetime

load_dotenv()

#TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = 1072469507504873492

class Repeater(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @tasks.loop(seconds=10)
    async def repeater(self):
        #channel = self.client.get_channel(CHANNEL)
        await self.channel.send(datetime.datetime.now().strftime("It's %H:%M.%S"))
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(CHANNEL)
        
        print('starting repeater')
        self.repeater.start()
    
def setup(client):
    client.add_cog(Repeater(client))

# --- main ---
intents = discord.Intents.all()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix='!', description="This is a helper bot",intents= intents)
setup(client)

print('starting bot')
client.run(format(env['BOT_TOKEN']))