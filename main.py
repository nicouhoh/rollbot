##### imports
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

    client = discord.Client
    # got to look up, seemed to work without it but seems weird still. 

    ##### Helper Functions ######
    #############################

    #print in console that we are ready when bot turns on
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print('------')

    #dice roll function 
    async def dice(self, input, message):

        roll = input.split('roll', 1)[1]

        if(roll.split('d')[0] == " " or roll.split('d')[0] == "" ):
            num = 1
        elif(len(roll.split('d')[0]) > 3):
            pass
        else:
            num = int(float(roll.split('d')[0]))

        sides = int(float(roll.split('d')[1]))

        await message.channel.send(str(message.author.name) + " rolled " +str(roll))

        total = 0

        rolls = range(1,num + 1)

        for n in rolls:
            rolled_num = random.randint(1,sides)
            await message.channel.send(rolled_num)
            total = rolled_num + total


        await message.channel.send(f'{str(message.author)} rolled a total of ' + str(total))  
        return total

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
            await self.dice(msg, message)

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
            player = message.author
            sheet = collection.find_one({"player": player.name}) # data is just the parsed out bit and deleteing it wont affect the db
            if sheet:
                await message.channel.send(f"are you sure you want to delete your character {sheet['name']} - Y / N ")
                answer = await client.wait_for('message')

                if answer.content.upper() == 'Y':
                    await message.channel.send('your character sheet has been destroyed')
                    collection.delete_one({"player": player.name})
                else:
                    await message.channel.send('character not deleted')
                    return 

            else:
                await message.channel.send('You do not have a player sheet, create one by typing "/create-char" into the chat.')

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

            player = message.author.name
            if collection.find_one({"player" : player}):
                await message.channel.send('You already have a character. If you want to make a new character, you need to delete your current character by typing "/delete-character".')
            
            else:
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
                        await message.channel.send(f"what is the dice throw for your {i}")
                        roll = await client.wait_for('message') #occasionally this reads the message from 132 as the wait_for message, need to make this only for message from player who started process. 
                        dice_roll = await self.dice(roll.content, message)
                        player_sheet[i] = dice_roll

                
                await message.channel.send('player sheet:')

                collection.insert_one({
                    "player" : player,      
                    "name": player_sheet['name'],
                    "look": player_sheet['look'],
                    "armor": 0,
                    "hitpoints": 0, 
                    "damage": 0,
                    "strength": player_sheet['strength'],
                    "dexterity": player_sheet['dexterity'],
                    "constitution": player_sheet['constitution'],
                    "inteligence": player_sheet['inteligence'],
                    "wisdom": player_sheet['wisdom'],
                    "charisma": player_sheet['charisma']
                    })

                sheet = collection.find_one({"player" : player})
                await message.channel.send(sheet)

client = MyClient()
client.run(os.environ['TOKEN'])

