import os
import random
import sys
import time

from constants import DIRECTIONS, COMMANDS
from helpers import slow_type
from items import Gold, Item
from locations import Location


# print a message slowly, wait for input
def slow_continue(message):
    input(message + "\n\n\t(press enter)")


# all locations
Location.ALL = {
    'big room': Location('The big room', 'This room is enormous. There are big fluffy things and a dragon.'),
    'food room': Location('The food room', 'Smells good in here.'),
    'long room': Location('The long room', 'You can\'t even see the end of this room. There are some big doors.'),
    'window room': Location('The window room', 'You are in the window room. There are big stands.'),
    'hiding room': Location('The hiding room', 'You are in the hiding room. There is a lot of hiding places.'),
    'grass room': Location('The grass room', 'You are in the grass room. There is a lot of grass and a wolf.'),
    'home': Location('Home', 'It’s the best house a mouse could have. There is a little bed made from scraps you collected from around the rooms. and a big pipe that is overhead that makes a little leak that’s perfect to wash your hands in. there is an empty pipe that sticks out. You could put the food you find or buy in.'),
}

# all location links
if Location.ALL:
    Location.ALL['big room'].add_link('north', 'food room')
    Location.ALL['big room'].add_link('east', 'window room')
    Location.ALL['big room'].add_link('west', 'grass room')
    Location.ALL['big room'].add_link('south', 'long room')
    Location.ALL['big room'].items.append(Gold(10))
    Location.ALL['big room'].items.append(Gold(20))

    Location.ALL['food room'].add_link('east', 'hiding room')
    Location.ALL['food room'].add_link('south', 'big room')
    Location.ALL['food room'].items.append(Item('cheese', 'a piece of cheese', 1))

    Location.ALL['long room'].add_link('east', 'window room')
    Location.ALL['long room'].add_link('west', 'big room')

    Location.ALL['window room'].add_link('north', 'hiding room')
    Location.ALL['window room'].add_link('west', 'big room')
    Location.ALL['window room'].add_link('south', 'long room')

    Location.ALL['hiding room'].add_link('north', 'home')
    Location.ALL['hiding room'].add_link('west', 'food room')
    Location.ALL['hiding room'].add_link('south', 'window room')

    Location.ALL['grass room'].add_link('east', 'big room')

    Location.ALL['home'].add_link('south', 'hiding room')


# inital state
inventory = []
current_location = Location.ALL['big room']
command = None
keep_playing = True

# game loop
while keep_playing:
    os.system('clear')

    if command == 'inventory':
        if inventory:
            print("Here's your inventory:")
            for i in inventory:
                print(f"\t{i.description}")
        else:
            print("You've not got anything.")

    current_location.print_state()

    # get player input
    print()
    user_input = input('> ').lower().split()
    action, obj = user_input[0], user_input[-1]
    command = COMMANDS.get(action)

    # do the thing
    if command:
        if command in DIRECTIONS:
            if command in current_location.linked_locations:
                location_id = current_location.linked_locations[command]
                current_location = Location.ALL[location_id]
            else:
                slow_continue('You cannot go that way.')

        elif command == 'drop':
            if inventory:
                new_inventory = []
                for i in inventory:
                    if obj == i.name.lower():
                        current_location.items.append(i)
                        print(f"You dropped {i.name}")
                    else:
                        new_inventory.append(i)

                if new_inventory == inventory:
                    slow_continue(f"You ain't got any {obj}.")

                inventory = new_inventory
            else:
                slow_continue("You ain't got nothing'.")

        elif command == 'get':
            items_in_room = [i.name.lower() for i in current_location.items]
            object_exists = obj in items_in_room

            if object_exists:
                items_to_put_back = []

                for item in current_location.items:
                    if item.name.lower() == obj:
                        inventory.append(item)
                    else:
                        items_to_put_back.append(item)

                current_location.items = items_to_put_back
                slow_continue(f'You picked up the {obj}.')

            else:
                slow_continue(f"{obj.capitalize()}? I don't see that here.")

        elif command == 'squeak':
            slow_continue("You squeaked at the monster.")

        elif command == 'exit':
            keep_playing = False
    else:
        unique_commands = set(COMMANDS.values())
        slow_continue('Try one of: ' + ', '.join(unique_commands))  # Show list of directions, separated by commas

print("Game over.")
