##### imports
# from replit import db
# will change all uses of db to Mongo DB  
import discord
import os
import random
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

URI = os.environ['MONGODB_URI']
cluster = MongoClient(URI)
db = cluster["Roll_bot"]
collection = db["character_sheets"]

### bot/ client  class 
class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print('------')

    async def dice(self, input, message):
        roll = input.split('roll', 1)[1]

        if(roll.split('d')[0] == " " or roll.split('d')[0] == "" ):
            num = 1
        else:
            num = int(float(roll.split('d')[0]))

        sides = int(roll.split('d')[1])

        await message.channel.send(str(message.author) + " rolled " +str(roll))

        total = 0

        rolls = range(1,num + 1)

        for n in rolls:
            rolled_num = random.randint(1,sides)
            total = rolled_num + total
            await message.channel.send(rolled_num)

        await message.channel.send(f'{str(message.author)} rolled a total of ' + str(total))  
        return total

    async def on_message(self, message):

        if message.author.id == self.user.id:
            return
        
        msg = message.content

        if msg.startswith('/hey'):
            await message.channel.send(f'Hello it is I {self.user.name}')
        
        #on message starts with /roll run roll function without putting total into another function
        if msg.startswith('/roll'):
            await self.dice(msg, message)

        #view player player_sheet
        if msg.startswith('/view-sheet'):

            player = str(message.author.name)

            if collection.find_one({"player": player}):
                sheet = collection.find_one({"player" : player})
                await message.channel.send(sheet["sheet"])

            else:
                await message.channel.send('You do not have a player sheet, create one by typing "/create-char" into the chat.')

    # delete character player_sheet

        if msg.startswith('/delete-character'):
            player = str(message.author)
            data = list(collection.find({}))[0][player] # data is just the parsed out bit and deleteing it wont affect the db
            if data:
                await message.channel.send(f"are you sure you want to delete your character {str(data['name'])} - Y / N ")
                answer = await client.wait_for('message')

                if answer.content.upper() == 'Y':
                    await message.channel.send('your character sheet has been destroyed')
                    # del 
                else:
                    await message.channel.send('character not deleted')
                    return 

            else:
                await message.channel.send('You do not have a player sheet, create one by typing "/create-char" into the chat.')

    ### build character sheet 
        if msg.startswith('/create-char'):

            player = message.author

            player_sheet = {
                "name": '',
                "look": '',
                "armor": 0,
                "hitpoints": 0, 
                "damage": 0,
                "strength": 0,
                "dexterity": 0,
                "constitution": 0,
                "inteligence": 0,
                "wisdom": 0,
                "charisma": 0
            }

            # need to check if player already has a character 
            await message.channel.send('Hello Traveler')
            
            for i in player_sheet:
                if i == "name":
                    await message.channel.send('What is your name ?')
                    name = await client.wait_for('message')
                    player_sheet["name"] = name.content
                elif i == "look":
                    await message.channel.send('Descibe your appearance.')
                    look = await client.wait_for('message')
                    player_sheet['look'] = look.content
                elif i == 'armor' or i == "hitpoints" or i == "damage":
                    player_sheet[i] = 0
                else:
                    await message.channel.send(f"roll for your {i}")
                    roll = await client.wait_for('message') #occasionally this reads the message from 132 as the wait_for message, need to make this only for message from player who started process. 
                    dice_roll = await self.dice(roll.content, message)
                    player_sheet[i] = dice_roll

            
            await message.channel.send('player sheet:')

            collection.insert_one({"player" : str(player.name), "sheet": player_sheet})
            sheet = collection.find_one({"player" : player.name})
            await message.channel.send(sheet["sheet"])

client = MyClient()
client.run(os.environ['TOKEN'])

