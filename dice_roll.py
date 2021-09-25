##### imports
import random
from pymongo import MongoClient
from dotenv import load_dotenv

# basic dice function 
# needs some bug fixes, new roll + atr function 
async def dice(client, input, message):

    roll = input.split('roll', 1)[1]

    if(roll.split('d')[0] == " " or roll.split('d')[0] == "" ):
        num = 1
    elif(len(roll.split('d')[0]) > 3):
        return # just stops function from running if it slices the string this way per the issue we've been having. 
    else:
        num = int(float(roll.split('d')[0]))

        sides = int(float(roll.split('d')[1]))

        await message.channel.send(str(message.author.name) + " rolled " +str(roll))

        total = 0

        rolls = range(1,num + 1)

        for n in rolls:
            rolled_num = random.randint(1,sides)
            await message.channel.send(rolled_num)
            # rolling hangs up the client with all these seprate messages, 
            # we should try sending 1 message that is created by the function, like the player-sheeet-reader()
            total = rolled_num + total


        await message.channel.send(f'{str(message.author)} rolled a total of ' + str(total))  
        return total
