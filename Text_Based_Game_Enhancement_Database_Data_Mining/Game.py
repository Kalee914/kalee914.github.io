from GameStats import GameStats

game = GameStats("Player") #initiate GameStats Class
game.show_player_status() #calling shower player status function in GameStats Class

while True:
    user_command = game.user_command

    if user_command == "exit": # game exit if users type exit
        break

    if user_command == 'north' or user_command == 'west' or user_command == 'south' or user_command == 'east':
        directions = game.rooms[game.current_room]  # extract the dict inside the dict
        # if user command is in the dictionary then change room with user command
        # else user command is not in the dictionary then print wrong direction
        if user_command in directions:
            game.current_room = directions[user_command]
            game.show_player_status()
        else:
            print("Oops! Wrong direction!")
            game.show_player_status()

    # Collect Items
    # welcome room does not have an item so current room can not be in welcome room to play this code
    elif game.current_room != 'Welcome Room' and user_command == ("grab " + game.rooms[game.current_room]['item']):
        item = game.rooms[game.current_room]['item']
        if item not in game.inventory:  # if the item is not in the list then add to the list by command
            game.inventory.append(item)
            print("Got it,", *item, " in the basket. GOOD JOB!", sep='')
            game.show_player_status()
        else:  # to avoid any duplication in the list
            print("This item is already in the basket.")
            game.show_player_status()
    else:
        print("Invalid Input")
        game.show_player_status()