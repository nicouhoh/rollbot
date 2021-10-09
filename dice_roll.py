##### imports
import os
import random
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

URI = os.environ['MONGODB_URI']
cluster = MongoClient(URI)
db = cluster["Roll_bot"]
collection = db["character_sheets"]

# basic dice function 
# needs new roll + atr function 
async def dice(input, message):

    roll = input.split('roll', 1)[1]
    
    sheet = collection.find_one({'player': message.author.name})

    if(roll.split('d')[0] == " " or roll.split('d')[0] == "" ):
        num = 1
    else:
        num = int(float(roll.split('d')[0]))

        sides = int(float(roll.split('d')[1]))

        total = 0

        rolls = range(1,num + 1)
        
        rolling_txt = ""

        for n in rolls:
            rolled_num = random.randint(1,sides)
            rolling_txt = rolling_txt + f"... {rolled_num} "
            total = rolled_num + total

        await message.channel.send(f"{sheet['name']} ({message.author.name}) rolled {str(roll)} \n {rolling_txt} \n a total of {str(total)}")  
        return total

async def roll_plus_attr(input, message):

    temp = input.split('roll', 1)[1]

    roll = temp.split('+ ')[0]
    attr = temp.split('+ ')[1]

    sheet = collection.find_one({'player': message.author.name})

    if(roll.split('d')[0] == " " or roll.split('d')[0] == "" ):
        num = 1
    else:
        num = int(float(roll.split('d')[0]))

        sides = int(float(roll.split('d')[1]))

        total = 0

        rolls = range(1,num + 1)
        
        rolling_txt = ""

        for n in rolls:
            rolled_num = random.randint(1,sides)
            rolling_txt = rolling_txt + f"... {rolled_num} "
            total = rolled_num + total

        if int(sheet[attr]) < 3:
            total -= 3
        elif int(sheet[attr]) <= 5:
            total -= 2
        elif int(sheet[attr]) <= 8:
            total -= 1
        elif int(sheet[attr]) <= 12:
            total = total
        elif int(sheet[attr]) <= 15:
            total += 1
        elif int(sheet[attr]) <= 17:
            total += 2
        elif int(sheet[attr]) > 17:
            total += 3

        await message.channel.send(f"{sheet['name']}({message.author.name}) rolled {str(roll)} \n {rolling_txt} \n andf their {attr} modifier makes it a total of {str(total)}")  
        return total + int(sheet[attr]) 


    await message.channel.send(f"roll var: {roll} attr var: {attr}")

async def roll_damage(input, message, client):

    sheet = collection.find_one({'player': message.author.name})
    dice = sheet['damage']

    max = int(dice.split('d', 1)[1])
    rolled = random.randint(1,max)
    rolling_txt = f"... {rolled} "

    await message.channel.send(f"{sheet['name']} rolled {dice} for damage \n {rolling_txt} \n do you need to roll additional dice? Y/N")
    answer = await client.wait_for('message')

    if answer.content.upper() == 'Y':
        await message.channel.send('roll')
        roll = await client.wait_for('message', check=lambda msg: msg.author.name == sheet["player"]) 

        num = int(float(roll.content.split('d')[0]))
        sides = int(float(roll.content.split('d')[1]))

        rolling_text = ""
        for n in range(num):
            roll = random.randint(1,sides)
            rolled += roll
            rolling_text += f"... {roll}"
            
        await message.channel.send(f"{rolling_text} \n {sheet['name']} did {rolled} damage")

    else:
        return 

