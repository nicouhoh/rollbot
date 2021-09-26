async def player_sheet_reader(message, data):
    text = "----------------------------------\n"
    for key in data:
        if key == "_id" or key == "player":
            pass
        elif key == "look" or key == "damage" or key == "charisma":
            text = text + f"---- {key} : {data[key]} ---- \n ---------------------------------- \n"
        else:
            text = text + f"---- {key} : {data[key]} ---- \n"
    await message.channel.send(text)
        # maybe instead of making this giant string like so we can loop over the obj and concatanate the string adding the \n when i say
