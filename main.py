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
db = MongoClient(URI)

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
            num = int(roll.split('d')[0])

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

            player = str(message.author)
            keys = list(db.keys()) # keys does not exist will need new syntax to work with MongoDBClient

        # db not working without repl.it db
        if player in keys:
            await message.channel.send(dict(db[player]))

        else:
            await message.channel.send('You do not have a player sheet, create one by typing "/create-char" into the chat.')

    # delete character player_sheet

        if msg.startswith('/delete-character'):
            player = str(message.author)
            data = db[player]

        if data:
            await message.channel.send(f"are you sure you want to delete your character {str(data['name'])} - Y / N ")
            answer = await client.wait_for('message')

            if answer.content.upper() == 'Y':
                await message.channel.send('your character sheet has been destroyed')
                del db[player]
            else:
                await message.channel.send('character not deleted')
                return 

        else:
            await message.channel.send('You do not have a player sheet, create one by typing "/create-char" into the chat.')

    ### build character sheet with charsheet class
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


        await message.channel.send('Hello Travler')
        # await message.channel.send(player)
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
                roll = await client.wait_for('message')
                dice_roll = await self.dice(roll.content, message)
                player_sheet[i] = dice_roll

        
        await message.channel.send('player sheet:')
        ## we can save the player sheet in the repl db or in whatever db we use in the final product
        ## this line lets us save it under the players discord name in our database. 
        
        #anything calling db is currently not working because of migration off repl.it
        db[player] = player_sheet
        await message.channel.send(db[f"{player}"])

client = MyClient()
client.run(os.environ['TOKEN'])

