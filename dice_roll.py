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
    # elif(len(roll.split('d')[0]) > 3):
    #     return # just stops function from running if it slices the string this way per the issue we've been having. 
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

        await message.channel.send(f"{message.author.name} rolled {str(roll)} \n {rolling_txt} \n {message.author.name} rolled a total of {str(total)}")  
        return total
