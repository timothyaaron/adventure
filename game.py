import random
import sys
import time

from items import Gold

directions = ['north', 'west', 'east', 'south']


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
                slow_type(item.description)

        # print where we can go
        print()
        for link_direction, linked_location in self.linked_locations.items():
            slow_type(link_direction + ': ' + locations[linked_location].name)


# all locations
locations = {
    'big room': Location('The big room', 'You are in the big room. There are big fluffy things and a dragon.'),
    'food room': Location('The food room', 'You are in the food room. There is cheese.'),
    'long room': Location('The long room', 'You are in the long room. There are some big doors.'),
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

    locations['food room'].add_link('east', 'hiding room')
    locations['food room'].add_link('south', 'big room')

    locations['long room'].add_link('east', 'window room')
    locations['long room'].add_link('west', 'big room')

    locations['window room'].add_link('north', 'hiding room')
    locations['window room'].add_link('west', 'big room')
    locations['window room'].add_link('south', 'long room')

    locations['hiding room'].add_link('west', 'food room')
    locations['hiding room'].add_link('south', 'window room')

    locations['grass room'].add_link('east', 'big room')


# player will start here
current_location = locations['big room']

# game loop
while True:
    current_location.print_state()

    # Read player input
    command = input('>').lower()
    if command in directions:
        if command not in current_location.linked_locations:
            print('You cannot go that way')
        else:
            location_id = current_location.linked_locations[command]
            current_location = locations[location_id]
    else:
        print('Try one of: ' + ', '.join(directions))  # Show list of directions, separated by commas
