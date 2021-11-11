async def player_sheet_reader(message, data):
    text = "----------------------------------\n"
    
    bonds = ""
    inventory = f"\n -------------| Inventory |------------- \n \n"
    for b in data["bonds"]:
        bonds = bonds + f"-- {b} -- \n"

    for i in data["inventory"]:
        if i["info"] == "special-item":
            inventory = inventory + "---" + i["name"] + " : "+ i["description"] + "---\n"
        elif i["info"] == "weapon":
            inventory = inventory + "---" + i["name"] + "\n + damage: "+ str(i["damage"]) + "\n"
        else:
            inventory = inventory + "---" + i["name"] + "---\n"

    for key in data:
        if key == "_id" or key == "player":
            pass
        elif key == "look" or key == "damage" or key == "charisma":
            text = text + f"---- {key} : {data[key]} ---- \n ---------------------------------- \n"
        elif key == "bonds":
            text = text + f"-------------| Bonds |------------- \n \n {bonds}"
        elif key == "inventory":
            text = text + inventory
        else:
            text = text + f"---- {key} : {data[key]} ---- \n"
    await message.channel.send(text)