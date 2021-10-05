# ROLL_BOT

A Discord bot for playing Powered by the Apocalypse RPG engine games easily and remotely. 
The first version of this bot with focus specificly on Dungeon World. Later it be expanded to include mechanics from Apocalypse World, and have more flexiblity to accomodate other games built with the Powered by the Apocalypse engine. 

## Commands
+ /hey - ping the bot make sure it is online
+ /create-char - walks a player through the character creation process and saves the players charactersheet on the backend.
+ /view-shet - prints the players character-sheet into the discord chat.
+ /delete-character - confirms if you are sure and then deletes players character sheet.
+ /lvl-up - allows a player to update their character sheet
+ /roll - roll dice function use _d_ syntax ex: "/roll 2d6" this will roll two six sided dice and print the output into the chat.
+ /roll { _d_ } + attr - roll function that follows the same syntax as above but also include the value of characters stats. ex: "/roll 2d6 + dexterity" will roll two six sided dice plus the players dexterity modifier. 

## Planned Changes
  + Will be adding character class, inventory, bonds, alignment, and class specific moves to character sheets. 
  + Will add basic moves to be either implimented with a '/hack-and-slash' type command similar to /roll or a '/basic-moves' command that will print all the relevant info about the basic moves
