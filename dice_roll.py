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

async def dice(client, input, message):

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
