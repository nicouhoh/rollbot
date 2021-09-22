##### imports
import discord
import os
from character_sheet import create_character, delete_sheet, lvl_up, view_sheet
from dice_roll import dice

### bot/ client  class 
class MyClient(discord.Client):

    client = discord.Client

    #print in console that we are ready when bot turns on
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print('------')

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
            await dice(self, msg, message)

        #############################################
        ########### Character-sheet functions 

        #view player player_sheet
        if msg.startswith('/view-sheet'):
            await view_sheet(message)
    
        # delete character player_sheet
        if msg.startswith('/delete-character'):
            await delete_sheet(self, message)
            
        ## update 
        if msg.startswith('/lvl-up'):
            await lvl_up(self, message)

        ##create character sheet
        if msg.startswith('/create-char'):
            await create_character(self, message)

        ################################################


client = MyClient()
client.run(os.environ['TOKEN'])

