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

        total += int(sheet[attr])

        await message.channel.send(f"{sheet['name']}({message.author.name}) rolled {str(roll)} \n {rolling_txt} \n plus their {attr}: {sheet[attr]} for a total of {str(total)}")  
        return total + int(sheet[attr]) 


    await message.channel.send(f"roll var: {roll} attr var: {attr}")