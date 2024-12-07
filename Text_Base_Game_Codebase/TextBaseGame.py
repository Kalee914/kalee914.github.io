# Kalee Li
#IT140
# sample fuction showing the goal of the game and move comands
def show_instruction():
    # print a main menu and the commands
    print("Welcome to Don't Wake Dad Game!")
    print("Pick up 6 messy items to clean the house before Dad wakes up!")
    print('Instruction:')
    print("Move commands: south, north, east, west")
    print("Add items to basket: grab 'item'")
    print("Type 'exit' to quit anytime ")
    print()

# to show player_status
# current rooms
# items in the room
# item in inventory
# game over status
# winning status
def show_player_status():
    global user_command
    if current_room == "Welcome Room":
        print()
        print("You are in the", current_room)
        print("Basket :", inventory)
        print("-" * 30)
        user_command = input("Enter your move: ")
    if current_room == 'Kitchen' or current_room == 'Living Room' or current_room == 'Office' or current_room == 'Bathroom' or current_room == "Trinity's Bedroom" or current_room == "Travis's Bedroom":
        print()
        print("You are in the", current_room)
        print("Basket :", inventory)
        if rooms[current_room]['item'] not in inventory:
            print('You see', rooms[current_room]['item']) # if item is not in inventory then print
        if len(inventory) == 6:
            print("*"*100)
            print("Congratulation! You have cleaned all the rooms and did not wake dad! "
                  "Thank you for helping the sibling!")
            print("*" * 100)
            exit()
        print("-" * 30)
        user_command = input("Enter your move: ")
    if current_room == "Parent's Room":
        print()
        print ("!"*30)
        print("You are in the", current_room)
        print("You Woke Dad!\nGAME OVER!\nThank you for playing, hope you enjoyed the game!")
        print("!" * 30)
        print()
        exit()


# dictionary for the rooms and items
rooms = {
    'Welcome Room': {'south': 'Living Room', 'north': 'Bathroom', 'east': 'Office', 'west': 'Kitchen'},
    'Kitchen': {'east': 'Welcome Room', "item": "toothpaste"},
    'Living Room': {'north': 'Welcome Room', 'east': "Travis's Bedroom", "item": "toilet paper"},
    'Office': {'north': "Parent's Room", 'west': 'Welcome Room', "item": "dirty laundry"},
    'Bathroom': {'south': 'Welcome Room', 'east': "Trinity's Bedroom", "item": 'burritos'},
    "Trinity's Bedroom": {'west': 'Bathroom', 'item': "cooking pans"},
    "Travis's Bedroom": {'west': 'Living Room', 'item': "burnt toaster"},
    "Parent's Room": {'item': 'DAD!'}  # Game over
}



# CODE START
current_room = 'Welcome Room'
user_command = ""
inventory = []  # empty list for user_command item
show_instruction()
show_player_status()

# exit mode
while user_command != "exit":
    # move around the rooms
    if user_command == 'north' or user_command == 'west' or user_command == 'south' or user_command == 'east':
        directions = rooms[current_room]  # extract the dict inside the dict
        if user_command in directions:
            current_room = directions[user_command]  # change room with user command
            show_player_status()
        else:
            print("Oops! Wrong direction!")
            show_player_status()
    # Collect Items
    # welcome room does not have an item so current room can not be in welcome room to play this code
    elif current_room != 'Welcome Room' and user_command == ("grab " + rooms[current_room]['item']):
        item = rooms[current_room]['item']
        if item not in inventory: # if the item is not in the list then add to the list by command
            inventory.append(item)
            print("Got it,", *item, " in the basket. GOOD JOB!", sep='')
            show_player_status()
        else: # to avoid any duplication in the list
            print("This item is already in the basket.")
            show_player_status()
    else:
        print("Invalid Input")
        show_player_status()




