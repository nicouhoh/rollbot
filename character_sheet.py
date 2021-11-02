##### imports
import discord
import os
from pymongo import MongoClient
from dotenv import load_dotenv

from printer import player_sheet_reader
from character_classes import class_list, barbarian, bard, cleric, druid, fighter, immolator

load_dotenv()

URI = os.environ['MONGODB_URI']
cluster = MongoClient(URI)
db = cluster["Roll_bot"]
collection = db["character_sheets"]

##### helper function #############

def class_damage(i):
    switch = {
        'barbarian': barbarian['damage'],
        'bard': bard['damage'],
        'cleric': cleric['damage'],
        'druid': druid['damage'],
        'fighter': fighter['damage'],
        'immolator': immolator['damage'],
    }
    return str(switch.get(i))

def class_bonds(i):
    switch = {
        'barbarian': barbarian['bonds'],
        'bard': bard['bonds'],
        'cleric': cleric['bonds'],
        'druid': druid['bonds'],
        'fighter': fighter['bonds'],
        'immolator': immolator['bonds'],
    }
    return switch.get(i)
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
            "class": '',
            "armor": 0,
            "hitpoints": 0, 
            "damage": 0,
            "strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "inteligence": 0,
            "wisdom": 0,
            "charisma": 0,
            "bonds": []
            }

        # starting_stats = ['16(+2)','15(+1)','13(+1)','12(-)', '9(-)', '8(-1)']
        starting_stats = ['16','15','13','12', '9', '8']

        await message.channel.send('Hello Traveler')
                
        for i in player_sheet:
            if i == "name":
                await message.channel.send('What is your name ?')
                name = await client.wait_for('message') 
                #possible update to listen to only response of player but does not seem to work
                player_sheet["name"] = name.content
            elif i == "look":
                await message.channel.send('Descibe your appearance.')
                look = await client.wait_for('message')
                player_sheet['look'] = look.content
            elif i == 'armor' or i == "hitpoints" or i == "damage" or i == "bonds":
                pass
            elif i == "class":
                await message.channel.send(f" choose your character's class from this list: {class_list}")

                valid_ans = False
                while valid_ans == False:
                    response = await client.wait_for('message')

                    if response.content in class_list:
                        player_sheet[i] = response.content
                        player_sheet['damage'] = class_damage(response.content)
                        player_sheet['bonds'] = class_bonds(response.content)
                        valid_ans = True
                    else:
                        await message.channel.send(f'choose a valid class {class_list}')
            else:
                await message.channel.send(f"choose a value from this list: {starting_stats} to assign to your {i}")

                valid_ans = False
                while valid_ans == False:
                    response = await client.wait_for('message')

                    if response.content in starting_stats:
                        starting_stats.pop(starting_stats.index(response.content))
                        player_sheet[i] = response.content
                        valid_ans = True
                    else:
                        await message.channel.send(f'choose a valid value {starting_stats}')

                
        await message.channel.send('player sheet:')

        collection.insert_one({
            "player" : player,      
            "name": player_sheet['name'],
            "look": player_sheet['look'],
            "class": player_sheet["class"],
            "armor": 0,
            "hitpoints": 0, 
            "damage": player_sheet['damage'],
            "strength": player_sheet['strength'],
            "dexterity": player_sheet['dexterity'],
            "constitution": player_sheet['constitution'],
            "inteligence": player_sheet['inteligence'],
            "wisdom": player_sheet['wisdom'],
            "charisma": player_sheet['charisma'],
            "bonds" : player_sheet['bonds'],
            })

        sheet = collection.find_one({"player" : player})
        await player_sheet_reader(message, sheet)
########## Read /view-sheet

async def view_sheet(message):
    player = message.author.name

    if collection.find_one({"player": player}):
        sheet = collection.find_one({"player" : player})
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
        "class": sheet['class'],
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
        if key == '_id' or key == 'player' or key == "class":
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

############# Bonds 
async def bonds(client, message):
    player = message.author
    sheet = collection.find_one({"player": player.name})

    bonds = class_bonds(sheet["class"])
    guild = client.get_guild(player.guild.id)
    players = []

    for member in guild.members:
                
        # if str(member.status) == 'online' and member.bot != True and member.name != player.name:
        # temp change for dev when this is done un comment above line and remove line below
        if member.bot != True and member.name != player.name:
            # memb_sheet = collection.find_one({"player": member.name})
            # players.append(str(memb_sheet["name"]))
            # in theory I think this should work but, no one eles has character sheets for me to try with :( 
            players.append(member.name)

    for i,b in enumerate(bonds):

        txt = f"selected a player from this list {players} for your bond: \n"
        await message.channel.send(txt + b)

        response = await client.wait_for('message')

        if response.content.lower() in players:
            players.pop(players.index(response.content.lower()))
            bonds[i] = bonds[i].replace('character-name', response.content)

    sheet['bonds'] = bonds
    collection.replace_one({'player': player.name }, sheet, upsert=False)
    await player_sheet_reader(message, sheet)

    
############## Delete /delete-character/

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
