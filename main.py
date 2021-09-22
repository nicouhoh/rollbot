##### imports
import discord
import os
import random
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from character_sheet import create_character, delete_sheet
from dice_roll import dice
load_dotenv()

URI = os.environ['MONGODB_URI']
cluster = MongoClient(URI)
db = cluster["Roll_bot"]
collection = db["character_sheets"]

### bot/ client  class 
class MyClient(discord.Client):

    client = discord.Client
    # got to look up, seemed to work without it but seems weird still. 

    #print in console that we are ready when bot turns on
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print('------')

    ### on_message responses ####
    async def on_message(self, message):

        # check that the message is not from the bot
        if message.author.id == self.user.id:
            return
        
        msg = message.content

        #ping bot the check its on / working
        if msg.startswith('/hey'):
            await message.channel.send(f'Hello it is I {self.user.name}')
        
        #run roll function without passing return value to another function
        if msg.startswith('/roll'):
            await dice(self, msg, message)

        #view player player_sheet
        if msg.startswith('/view-sheet'):

            player = message.author.name

            if collection.find_one({"player": player}):
                sheet = collection.find_one({"player" : player})
                await message.channel.send(sheet)

            else:
                await message.channel.send('You do not have a player sheet, create one by typing "/create-char" into the chat.')

    # delete character player_sheet

        if msg.startswith('/delete-character'):
            await delete_sheet(self, message)
            
        ## update 

        if msg.startswith('/lvl-up'):

            player = message.author
            sheet = collection.find_one({"player" : player.name})
            
            player_sheet = {
                "player" : sheet['player'],      
                "name": sheet['name'],
                "look": sheet['look'],
                "armor": sheet['armor'],
                "hitpoints": sheet['hitpoints'], 
                "damage": sheet['damage'],
                "strength": sheet['strength'],
                "dexterity": sheet['dexterity'],
                "constitution": sheet['constitution'],
                "inteligence": sheet['inteligence'],
                "wisdom": sheet['wisdom'],
                "charisma": sheet['charisma']
            }
            for key in player_sheet:
                if key == '_id' or key == 'player':
                    pass
                else:
                    await message.channel.send(f" would you like to update your {key}? y/n")
                    answer = await client.wait_for('message')#wait_for(message, check = check) need to define def check that checks the message.authour is == to the author who started the command. or player in our context
                    if answer.content.upper() == 'Y':
                        await message.channel.send(f" {key}:{player_sheet[key]} should equal what?")
                        update_answer = await client.wait_for('message')
                        player_sheet[key] = update_answer.content
                        collection.replace_one({'player': player.name }, player_sheet, upsert=False)
                    else:
                        await message.channel.send('okay then')

    ### build character sheet
        if msg.startswith('/create-char'):
            await create_character(self, message)

client = MyClient()
client.run(os.environ['TOKEN'])

