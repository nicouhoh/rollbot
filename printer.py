async def player_sheet_reader(message, data):
    text = "----------------------------------\n"
    
    bonds = ""
    for b in data["bonds"]:
                bonds = bonds + f"-- {b} -- \n"

    for key in data:
        if key == "_id" or key == "player":
            pass
        elif key == "look" or key == "damage" or key == "charisma":
            text = text + f"---- {key} : {data[key]} ---- \n ---------------------------------- \n"
        elif key == "bonds":
            text = text + f"---- {key} ---- \n {bonds}"
        else:
            text = text + f"---- {key} : {data[key]} ---- \n"
    await message.channel.send(text)