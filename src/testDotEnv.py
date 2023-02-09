import os
import sys
#from dotenv import load_dotenv
#load_dotenv()
#TOKEN = os.getenv('BOT_TOKEN')
#print(TOKEN)
#print(os.environ['BOT_TOKEN'])

from os import environ as env

from dotenv import load_dotenv
load_dotenv()

print('BOT_TOKEN:  {}'.format(env['BOT_TOKEN']))
#print('HOSTNAME: {}'.format(env['HOSTNAME']))
#print('PORT:     {}'.format(env['PORT']))
'''
try:  
  os.environ['BOT_TOKEN']
except KeyError: 
  print('[error]: `BOT_TOKEN` environment variable required')
  sys.exit(1)

'''