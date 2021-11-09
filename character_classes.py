class_list = ['barbarian', 'bard', 'cleric', 'druid', 'fighter', 'immolator', 'paladin', 'ranger', 'thief', 'wizard' ]


barbarian = {
    'hp': 8,
    'damage': 'd10',
    'bonds': [
        "character-name is puny and foolish, but amusing to me.", 
        "character-name's ways are strange and confusing.", 
        "character-name is always getting into trouble - I must protect them from themselves.",
        "character-name shares my hunger for glory; the earth will tremble at our passing!",
    ],
    'starting-gear': [
        {
            "name":"dungeon rations",
            "info": "gear",
            "uses": 5, 
            "weight":1 
        },
        {
            "name":"dagger",
            "info": "weapon",
            "attr": ["hand"],
            "damage": 0,
            "weight": 1
        },
        {
            "name": "Token",
            "info": "special-item",
            "prompt": "A token of where you've traveled or where you are from.",
            "description": ""
        },
        [ 
            {
                "name":"Axe",
                "info": "weapon",
                "attr": ["close"],
                "damage": 0,
                "weight": 1
            },
            {
                "name":"Two-handed Sword",
                "info": "weapon",
                "attr": ["close"],
                "damage": 1,
                "weight": 2
            }
        ],
        [
            {
            "name": "Adventuring Gear", 
            "info": "gear",
            "uses": 5, 
            "weight":1 
            },
            {
            "name": "Chainmail", 
            "info": "armor",
            "armor": 1, 
            "weight":1  
            }
        ]
    ] 
    # we are going to try loop over the starting gear and push anything that is not an array 
    # to the players sheet["inventory"], 
    # if the index is an array we will ask the player to choose between the items. 
    # based on the value of info we can ask for imformation as needed, ie with the Token will prompt the user to describe the item 
    #  then push that object with the response as the description to the players inventory.

}
bard = {
    'hp': 6,
    'damage': 'd6',
    'bonds' : [
        "This is not my first adventure with character-name.",
        "I sang stories of character-name long before i ever met them in person.",
        "character-name is often the butt of my jokes.",
        "I am writting a ballad about the adventures of character-name."
    ],
}
cleric = {
    'hp': 8,
    'damage': 'd6',
    'bonds' : [
        "character-name has insluted my deity; I do ot trust them.",
        "character-name is a good and faithful person; I trust them implicity",
        "character-name is in constant danger, I will keep them safe.",
        "I am working on converting character-name to my faith."
    ],
}
druid = {
    'hp': 6,
    'damage': 'd6',
    'bonds': [
        "character-name smells more like prey than a hunter.",
        "The spirits spoke to me of a great danger that follows character-name.",
        "I have shown character-name a secret rite of the land.",
        "character-name has tasted my blood and I theirs. We are bound by it."
    ],
}
fighter = {
    'hp': 10,
    'damage': 'd10',
    'bonds': [
        "character-name owes me their life, whether they admit it or not.",
        "I have sworn to protect character-name",
        "I worry about the ability of character-name to survice in the dungeon",
        "character-name is soft, but I will make them hard like me"
    ]
}
immolator = {
    'hp': 4,
    'damage': 'd8',
    'bonds': [
        "character-name has felt the hellish touch of fire, now they know my strength.",
        "I will teach character-name the true meaning of sacrifice.",
        "I cast somthing into the fire for character-name and still owe them their due."
    ]
}
paladin = {
    'hp': 10,
    'damage': 'd10',
    'bonds': [
        "character-name's misguided behavior endangers their very soul!",
        "character-name has stoof by me in battle and can be trusted completely.",
        "I respect the beliefs of character-name but hope they someday see the true way.",
        "character-name is a brave soul, I have much to learn from them"
    ]
}
ranger = {
    'hp': 8,
    'damage': 'd8',
    'bonds': [
        "I have guided character-name before and they owe me for it.",
        "character-name is a friend of nature, so I will be their friend as well.",
        "character-name has no respect for nature so I have no respect for them.",
        "character-name does not understand life in the wild so I will teach them"
    ]
}
thief = {
    'hp': 6,
    'damage': 'd8',
    'bonds': [
        "I stole something from character-name",
        "character-name has my back when things go wrong",
        "character-name knows incriminating details about me.",
        "character-name and I have a con running"
    ]
}
wizard = {
    'hp': 4,
    'damage': 'd4',
    'bonds': [
        "character-name will play an important role in the events to come. I have seen it!",
        "character-name is keeping an immportant secret from me.",
        "character-name is woefully misinformed about the world; I will teach them all that I can.",
        
    ]
}
