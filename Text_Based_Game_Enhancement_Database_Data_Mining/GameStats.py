from PlayerStatsDB import PlayerStatsDB

class GameStats:
    def __init__(self, name):
        self.name = name
        self.db = PlayerStatsDB()
        self.inventory = []
        self.current_room = "Welcome Room"
        self.user_command = None
        self.gamer_tag = None

        # dictionary for the rooms and items (directory)
        self.rooms = {
            'Welcome Room': {'south': 'Living Room', 'north': 'Bathroom', 'east': 'Office', 'west': 'Kitchen'},
            'Kitchen': {'east': 'Welcome Room', "item": "toothpaste"},
            'Living Room': {'north': 'Welcome Room', 'east': "Travis's Bedroom", "item": "toilet paper"},
            'Office': {'north': "Parent's Room", 'west': 'Welcome Room', "item": "dirty laundry"},
            'Bathroom': {'south': 'Welcome Room', 'east': "Trinity's Bedroom", "item": 'burritos'},
            "Trinity's Bedroom": {'west': 'Bathroom', 'item': "cooking pans"},
            "Travis's Bedroom": {'west': 'Living Room', 'item': "burnt toaster"},
            "Parent's Room": {'item': 'DAD!'}  # Game over
        }

    def show_instruction(self):
        # print a main menu and the commands
        print("Welcome to Don't Wake Dad Game!")
        print("Pick up 6 messy items to clean the house before Dad wakes up!")
        print('Instruction:')
        print("Move commands: south, north, east, west")
        print("Add items to basket: grab 'item'")
        print("Type 'exit' to quit anytime ")
        print()

    def handle_gamer_tag(self):
        # user prompt to enter gamer tag for stat report or choose play without stat
        print("Please enter your gamer tag for statistic tracking, or press enter to play without stats")
        # get user input and remove any whitespace
        self.gamer_tag = input("Enter your gamer tag:").strip()

        #check if user entered gamer tag, if user entered gamer tag, add new player to database
        if self.gamer_tag:
            self.db.add_player(self.gamer_tag)
            print(f"Gamer Tag '{self.gamer_tag}' registered. Your game stats will be tracked.")
            print() # Add space between output for readability
            print() # Add space between output for readability
            self.db.get_player_stats(self.gamer_tag) # Retrieve and display the player's stats from the database
        else:
            #if no gamer tag, print a message to indicate stats will not be track
            print("You chose to play without tracking stats")
        print()
        print()
        self.show_instruction() # Display game instructions after handling the gamer tag

    def show_player_status(self):
        # If the gamer tag has not been set, prompt the user to enter it
        if not self.gamer_tag:
            self.handle_gamer_tag()

        # If the player is in the "Welcome Room", display the room and inventory, and prompt for a move
        if self.current_room == "Welcome Room":
            print()
            print("You are in the", self.current_room)
            print("Basket :", self.inventory) #show the current inventory
            print("-" * 30)
            self.user_command = input("Enter your move: ") # Get the player's next move

        # If the player is in one of these rooms, display room details and inventory, and check for the item
        if self.current_room == 'Kitchen' or self.current_room == 'Living Room' or self.current_room == 'Office' or self.current_room == 'Bathroom' or self.current_room == "Trinity's Bedroom" or self.current_room == "Travis's Bedroom":
            print()
            print("You are in the", self.current_room)
            print("Basket :", self.inventory) # Show the current inventory (basket)

            # If the item for the current room is not in the inventory, display it to the player
            if self.rooms[self.current_room]['item'] not in self.inventory:
                print('You see', self.rooms[self.current_room]['item']) # Show item in the room if not in inventory

            # If the player has collected all 6 items, update stats, show a congratulatory message, and end the game
            if len(self.inventory) == 6:
                if self.gamer_tag:
                    self.db.update_stats(self.gamer_tag, win=True)  # Update winning stats
                print("*" * 100)
                print("Congratulation! You have cleaned all the rooms and did not wake dad! "
                      "Thank you for helping the sibling!")
                print("*" * 100)
                # if player entered gamer_tag show updated stats
                if self.gamer_tag:
                    self.db.get_player_stats(self.gamer_tag) # Show the player's stats
                exit() # End the game

            print("-" * 30)
            self.user_command = input("Enter your move: ")

        # If the player enters the "Parent's Room", end the game with a "Game Over" message
        if self.current_room == "Parent's Room":
            if self.gamer_tag:
                self.db.update_stats(self.gamer_tag, win=False) # update lost stats
            print()
            print("!" * 30)
            print("You are in the", self.current_room)
            print("You Woke Dad!\nGAME OVER!\nThank you for playing, hope you enjoyed the game!")
            print("!" * 30)

            # if player entered gamer_tag show updated stats
            if self.gamer_tag:
                self.db.get_player_stats(self.gamer_tag)
            print()

            exit() # End the game
