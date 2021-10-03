##### imports
import discord
import os
from pymongo import MongoClient
from dotenv import load_dotenv

from printer import player_sheet_reader
from dice_roll import dice

load_dotenv()

URI = os.environ['MONGODB_URI']
cluster = MongoClient(URI)
db = cluster["Roll_bot"]
collection = db["character_sheets"]

############ Create /create-char

async def create_character(client, message):
    player = message.author.name

    #check if player has char sheet
            
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

        starting_stats = ['16(+2)','15(+1)','13(+1)','12(-)', '9(-)', '8(-1)']
        # need to build out create character function to fill stats with these values instead of by rolling
        # when a player is asked to assign a value to a stat it should print all the remaining values to the chat,
        # after a value is selected it should not be printed when asking for the next stat. 

        await message.channel.send('Hello Traveler')
                
        for i in player_sheet:
            if i == "name":
                await message.channel.send('What is your name ?')
                name = await client.wait_for('message', check=lambda msg: msg.author.name == player) 
                #possible update to listen to only response of player but does not seem to work
                player_sheet["name"] = name.content
            elif i == "look":
                await message.channel.send('Descibe your appearance.')
                look = await client.wait_for('message')
                player_sheet['look'] = look.content
            elif i == 'armor' or i == "hitpoints" or i == "damage":
                player_sheet[i] = 0
            else:
                await message.channel.send(f"which value shall we assign to your {i}, {starting_stats}")
                answer = await client.wait_for('message') #occasionally this reads the message from 132 as the wait_for message, need to make this only for message from player who started process. 
                if answer.content in starting_stats:
                    starting_stats.pop(starting_stats.index(answer.content))
                    player_sheet[i] = answer.content 
                else:
                    await message.channel.send('that is not a valid input try again.')
                    answer = await client.wait_for('message') #occasionally this reads the message from 132 as the wait_for message, need to make this only for message from player who started process. 
                    # this doesn't add the stat to the sheet or remove it from the list when we make the mistake.
                    #this may need a helper function to deal with wrong inputs. 
                
        await message.channel.send('player sheet:')

        collection.insert_one({
            "player" : player,      
            "name": player_sheet['name'],
            "look": player_sheet['look'],
            "armor": 0,
            "hitpoints": 0, 
            "damage": 0, # should be assigned based on class player chooses is dice val d6, d10 etc... 
            "strength": player_sheet['strength'],
            "dexterity": player_sheet['dexterity'],
            "constitution": player_sheet['constitution'],
            "inteligence": player_sheet['inteligence'],
            "wisdom": player_sheet['wisdom'],
            "charisma": player_sheet['charisma']
            })

        sheet = collection.find_one({"player" : player})
        await player_sheet_reader(message, sheet)
########## Read /view-sheet

async def view_sheet(message):
    player = message.author.name

    if collection.find_one({"player": player}):
        sheet = collection.find_one({"player" : player})
        # await message.channel.send(sheet)
        await player_sheet_reader(message, sheet)
    else:
        await message.channel.send('You do not have a player sheet, create one by typing "/create-char" into the chat.')

############ Update /lvl-up

async def lvl_up(client, message):
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

    sheet = collection.find_one({"player" : player.name})          
    await player_sheet_reader(message, sheet)
    
############## Delete /delete-character

async def delete_sheet(client, message):
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
