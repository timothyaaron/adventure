import os
import random
import sys
import time

from items import Gold, Item

directions = ['north', 'west', 'east', 'south']
commands = {
    'n': 'north',
    's': 'south',
    'e': 'east',
    'w': 'west',
    'north': 'north',
    'south': 'south',
    'east': 'east',
    'west': 'west',

    'i': 'inventory',
    'inventory': 'inventory',

    'get': 'get',
    'grab': 'get',
    'pick': 'get',
    'take': 'get',

    # TODO: let player drop items
    # 'drop': 'drop',
    # 'put': 'drop',

    # TODO: let player exit
    # 'exit': 'exit',
    # 'quit': 'exit',
    # 'stop': 'exit',
}


# print a message slowly
def slow_type(message):
    typing_speed = 600  # wpm
    for m in message:
        sys.stdout.write(m)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/typing_speed)
    print()


# location name, description, and add_link function
class Location:
    # Constructor - set up
    def __init__(self, name, description):
        self.name = name
        self.description = description

        # Empty dictionary - will store which locations are linked to which other locations
        self.linked_locations = {}
        self.items = []

    def add_link(self, direction, destination):
        # Add link to linked_locations dictionary (if both are valid)
        if direction not in directions:
            raise ValueError('Invalid direction')
        elif destination not in locations:
            raise ValueError('Invalid destination')
        else:
            self.linked_locations[direction] = destination

    def print_state(self):
        # print where we are
        print()
        slow_type(self.description)

        if self.items:
            print()
            slow_type('There are items in this room...')
            for item in self.items:
                slow_type(f"\t{item.description}")

        # print where we can go
        print()
        for link_direction, linked_location in self.linked_locations.items():
            slow_type(link_direction + ': ' + locations[linked_location].name)


# all locations
locations = {
    'big room': Location('The big room', 'This room is enormous. There are big fluffy things and a dragon.'),
    'food room': Location('The food room', 'Smells good in here.'),
    'long room': Location('The long room', 'You can\'t even see the end of this room. There are some big doors.'),
    'window room': Location('The window room', 'You are in the window room. There are big stands.'),
    'hiding room': Location('The hiding room', 'You are in the hiding room. There is a lot of hiding places.'),
    'grass room': Location('The grass room', 'You are in the grass room. There is a lot of grass and a wolf.'),
}

# all location links
if locations:
    locations['big room'].add_link('north', 'food room')
    locations['big room'].add_link('east', 'window room')
    locations['big room'].add_link('west', 'grass room')
    locations['big room'].add_link('south', 'long room')
    locations['big room'].items.append(Gold(10))
    locations['big room'].items.append(Gold(20))

    locations['food room'].add_link('east', 'hiding room')
    locations['food room'].add_link('south', 'big room')
    locations['food room'].items.append(Item('cheese', 'a piece of cheese', 1))

    locations['long room'].add_link('east', 'window room')
    locations['long room'].add_link('west', 'big room')

    locations['window room'].add_link('north', 'hiding room')
    locations['window room'].add_link('west', 'big room')
    locations['window room'].add_link('south', 'long room')

    locations['hiding room'].add_link('west', 'food room')
    locations['hiding room'].add_link('south', 'window room')

    locations['grass room'].add_link('east', 'big room')


# inital state
inventory = []
current_location = locations['big room']
command = None

# game loop
while True:
    # TODO: clear screen, but get warning messages
    # os.system('clear')

    if command == 'inventory':
        print("Here's your inventory:")
        for i in inventory:
            print(f"\t{i.description}")

    current_location.print_state()

    # get player input
    print()
    user_input = input('>').lower().split()
    action, obj = user_input[0], user_input[-1]
    command = commands.get(action)

    # import pdb; pdb.set_trace()

    # do the thing
    if command:
        if command in directions:
            if command in current_location.linked_locations:
                location_id = current_location.linked_locations[command]
                current_location = locations[location_id]
            else:
                print('You cannot go that way.')
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
                print(f'You picked up the {obj}.')

            else:
                print(f"{obj.capitalize()}? I don't see that here.")
    else:
        unique_commands = set(commands.values())
        print('Try one of: ' + ', '.join(unique_commands))  # Show list of directions, separated by commas
