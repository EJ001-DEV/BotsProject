#import asyncio
#import discord
import sqlite3

#import aiosqlite
#import os
#from datetime import datetime
#from timer import Timer, TimerStatus
#################################
from os import environ as env
from dotenv import load_dotenv
#################################
from discord.ext import commands

COLOR_DANGER = 0xc63333
COLOR_SUCCESS = 0x33c633

#class DiscordDB():
load_dotenv()

class DiscordDB():

    def __init__(self):
        #self.bot = bot
        #self.timer = Timer()
        #self.db = sqlite3.connect(format(env['DBName']))
        self.create_tables()
        print('init')


    def create_tables(self):
        print('create table')
        self.db = sqlite3.connect(format(env['DBName']))
        cur = self.db.cursor()
        # Create table

        #cur.execute(format(env['SQLDB']))
        cur.execute('''
        CREATE TABLE IF NOT EXISTS channel2 (
            id integer PRIMARY KEY AUTOINCREMENT,
            username text NOT NULL,
            start_time text NOT NULL,
            delay text NOT NULL
            )
        ''')
        self.db.commit()

    #Split list
    def SplitStr(self, cText):
        cField = ''        
        for i in range(len(cText)):
            if i == len(cText)-1:
                cSeparator = ''
            else:
                cSeparator = ','

            cField = cField + cText[i] + cSeparator        
        return cField

    def ProcSelect(self, cTable : str, field, cWhere : str):
        
        #Split fields of select
        cField = self.SplitStr(field)
        
        if cWhere is not None:
            cSQL = 'Select ' + cField + ' from ' + cTable + ' Where ' + cWhere
        else:
            cSQL = 'Select ' + cField + ' from ' + cTable
        
        print(cSQL)
        #oData = []
        self.db = sqlite3.connect(format(env['DBName']))
        cur = self.db.cursor()        
        row = cur.execute(cSQL)
        #oData = row
        #for row in cur.execute(cSQL):
        #    #print(row[0] , row[1], row[2])        
        #    print(row)
        #self.db.close()
        return row

    def ProcInsert(self, cTable : str, field, ValueInsert):
        #Split fields of select
        cField = self.SplitStr(field)
        cValue = self.SplitStr(ValueInsert)
                
        cSQL = 'Insert into ' + cTable + '(' + cField + ') values (' + cValue + ')'
        print(cSQL)
        self.db = sqlite3.connect(format(env['DBName']))
        cur = self.db.cursor()        
        cur.execute(cSQL)        
        self.db.commit()
        self.db.close()
        print('Insert Done')

    def ProcUpdate(self, cTable : str, cField_cValue, cWhere : str):
        #Split fields of select
        #cField = self.SplitStr(field)
        #cValue = self.SplitStr(ValueInsert)
                
        cSQL = 'Update ' + cTable + ' Set ' + cField_cValue + ' Where ' + cWhere
        print(cSQL)
        self.db = sqlite3.connect(format(env['DBName']))
        cur = self.db.cursor()        
        cur.execute(cSQL)        
        self.db.commit()
        self.db.close()
        print('Update Done')        
        
def OperationDB(cOper : str, cTable : str, oField, oValue, cWhere : str):
    #construct the object
    oOperDB = DiscordDB()
    oData = None
    if cOper == 'SEL':#Select Table
        #oData = None
        oData = oOperDB.ProcSelect(cTable, oField, cWhere)        
        #oOperDB.ProcSelect(cTable: str, field: Any, cWhere: str)
    elif cOper == 'UPD':#Update Table
        oOperDB.ProcUpdate(cTable, oField, cWhere)
        #oOperDB.ProcUpdate(cTable: str, cField_cValue: Any, cWhere: str)
    elif cOper == 'INS':#Insert Table
        oOperDB.ProcInsert(cTable, oField, oValue)
        #oOperDB.ProcInsert(cTable: str, field: Any, ValueInsert: Any)
    return oData
#print('SQLDB:  {}'.format(env['SQLDB']))
#bot.run(format(env['BOT_TOKEN']))


##SQL SELECT
#oOperDB.ProcSelect('channel2', ['id','username','delay'], "Where username = 'EJ001'")
#oOperDB.ProcSelect('channel', ['id','username','delay'], 'Where  CAST(delay as integer) < 7')
#oOperDB.ProcSelect('channel2', ['id','username','delay'], 'Where  CAST(delay as integer) = 5 ')

##SQL INSERT
#Insert into VOICE_CHANNEL(IDCHANNEL, CHANNELNAME, DATEREG, CHANNELTYPE)VALUES('1071493291876552872','Lounge','2023-02-10','V')
#oOperDB.ProcInsert('VOICE_CHANNEL','IDCHANNEL, CHANNELNAME, DATEREG, CHANNELTYPE',"'1071493291876552872','Lounge','2023-02-10','V'")

##SQL UPDATE
#oOperDB.ProcUpdate("GAME", "DESCRIPTION = 'THREE QUESTIONS GAME'","IDGAME = 1")

##STATUS GAME: START GAME (STA), END GAME (END)
#oOperDB.ProcUpdate("GAME", "STATUS = 'STA'","IDGAME = 1")

#oOperDB.ProcUpdate("GAME", "STATUS = 'END', DATEENDGAME = '2023-02-11 16:34:52'","IDGAME = 1")

print('Job Finish')
