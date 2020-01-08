from django.contrib.auth.models import User
from charlie.models import Player, Room
from itertools import product
import random
import copy
import uuid

Room.objects.all().delete()

high_prob_rooms = [
    ('Hallway', 'A corridor with red emergency lights illuminating the room and the occasional sparks from loose wires'),
    ('Crew Cabin', 'A crew members cabin with a small mattress and mementos')
]

med_prob_rooms = [
    ('Mess Hall', 'A large room with tables for eating, food is everwhere'),
    ('Recreation Center', 'A room with excercise equipment and foosball tables'),
    ('Bathroom', 'The cleanest bathroom you\'ve ever seen')
]

low_prob_rooms = [
    ('Medical Bay', 'Lot of medical supplies still around'),
    ('Weapons', ''),
    ('Engineering Bay', 'Place of engineering')
]

single_rooms = [
    ('Engine Room', 'Home of engine'),
    ('Defense Center', 'Place of defense'),
    ('Command Center', 'Place of planning'),
    ('Captain Quaters', 'Captain\'s Hangout'),
    ('Bridge', 'Navigation Center')
]

width = 10
height = 10
coordinates = list(product(range(width), range(height)))

d = {}
min_coord = 0
max_coord = 9
all_rooms = []
for i in range(100):
    room_temp = {'id': i+1, 'title': '', 'desc': '', 'x': -1, 'y': -1,
                 'n_to': [], 'e_to': [], 's_to': [], 'w_to': []}
    room = ('None', 'None')
    cord = (-1, -1)
    room_n_to = (-1, -1)
    room_e_to = (-1, -1)
    room_s_to = (-1, -1)
    room_w_to = (-1, -1)

    room_prob = random.randint(1, 100)

    if i == 0:
        cord = (0, 0)
        room = single_rooms[0]
        

        room_temp['title'] = single_rooms[0][0]
        room_temp['desc'] = single_rooms[0][1]
        room_temp['x'] = cord[0]
        room_temp['y'] = cord[1]

        single_rooms.remove(room)
        coordinates.remove(cord)

    elif i == 1:
        cord = (1, 8)
        room = single_rooms[0]
        

        room_temp['title'] = single_rooms[0][0]
        room_temp['desc'] = single_rooms[0][1]
        room_temp['x'] = cord[0]
        room_temp['y'] = cord[1]

        single_rooms.remove(room)
        coordinates.remove(cord)

    elif i == 2:
        cord = (3, 6)
        room = single_rooms[0]
        

        room_temp['title'] = single_rooms[0][0]
        room_temp['desc'] = single_rooms[0][1]
        room_temp['x'] = cord[0]
        room_temp['y'] = cord[1]

        single_rooms.remove(room)
        coordinates.remove(cord)

    elif i == 3:
        cord = (7, 2)
        room = single_rooms[0]
        

        room_temp['title'] = single_rooms[0][0]
        room_temp['desc'] = single_rooms[0][1]
        room_temp['x'] = cord[0]
        room_temp['y'] = cord[1]

        single_rooms.remove(room)
        coordinates.remove(cord)

    elif i == 4:
        cord = (9, 9)
        room = single_rooms[0]
        

        room_temp['title'] = single_rooms[0][0]
        room_temp['desc'] = single_rooms[0][1]
        room_temp['x'] = cord[0]
        room_temp['y'] = cord[1]

        single_rooms.remove(room)
        coordinates.remove(cord)

    else:
        cord = random.choice(coordinates)
        #
        room_temp['x'] = cord[0]
        room_temp['y'] = cord[1]
        #
        coordinates.remove(cord)

        if room_prob < 60:
            room = random.choice(high_prob_rooms)

            room_temp['title'] = room[0]
            room_temp['desc'] = room[1]

        elif room_prob > 59 and room_prob < 90:
            room = random.choice(med_prob_rooms)

            room_temp['title'] = room[0]
            room_temp['desc'] = room[1]

        else:
            room = random.choice(low_prob_rooms)

            room_temp['title'] = room[0]
            room_temp['desc'] = room[1]


    # Left edge
    if room_temp['x'] == min_coord:

        # left, bottom corner x,y = 0
        if room_temp['y'] == min_coord:
            room_n_to = (room_temp['x'], room_temp['y'] + 1)
            room_e_to = (room_temp['x']+1, room_temp['y'])

            room_temp['n_to'] = (room_temp['x'], room_temp['y'] + 1)
            room_temp['e_to'] = (room_temp['x']+1, room_temp['y'])

        # left top corner, x=0, y=max
        if room_temp['y'] == max_coord:
            room_s_to = (room_temp['x'], room_temp['y'] - 1)
            room_e_to = (room_temp['x']+1, room_temp['y'])

            room_temp['s_to'] = (room_temp['x'], room_temp['y'] - 1)
            room_temp['e_to'] = (room_temp['x']+1, room_temp['y'])

        # far left middle
        else:
            room_n_to = (room_temp['x'], room_temp['y'] + 1)
            room_s_to = (room_temp['x'], room_temp['y'] - 1)
            room_e_to = (room_temp['x']+1, room_temp['y'])

            room_temp['n_to'] = (room_temp['x'], room_temp['y'] + 1)
            room_temp['s_to'] = (room_temp['x'], room_temp['y'] - 1)
            room_temp['e_to'] = (room_temp['x']+1, room_temp['y'])

    # Right edge
    elif room_temp['x'] == max_coord:

        # right bottom corner
        if room_temp['y'] == min_coord:
            room_n_to = (room_temp['x'], room_temp['y'] + 1)
            room_w_to = (room_temp['x']-1, room_temp['y'])

            room_temp['n_to'] = (room_temp['x'], room_temp['y'] + 1)
            room_temp['w_to'] = (room_temp['x']-1, room_temp['y'])

    # right top corner
        if room_temp['y'] == max_coord:
            room_s_to = (room_temp['x'], room_temp['y'] - 1)
            room_w_to = (room_temp['x']-1, room_temp['y'])

            room_temp['s_to'] = (room_temp['x'], room_temp['y'] - 1)
            room_temp['w_to'] = (room_temp['x']-1, room_temp['y'])

    # far right middle
        else:
            room_n_to = (room_temp['x'], room_temp['y'] + 1)
            room_s_to = (room_temp['x'], room_temp['y'] - 1)
            room_w_to = (room_temp['x']-1, room_temp['y'])

            room_temp['n_to'] = (room_temp['x'], room_temp['y'] + 1)
            room_temp['s_to'] = (room_temp['x'], room_temp['y'] - 1)
            room_temp['w_to'] = (room_temp['x']-1, room_temp['y'])

    # Top edge
    elif room_temp['y'] == max_coord:

        # Top right
        if room_temp['x'] == max_coord:
            room_s_to = (room_temp['x'], room_temp['y'] - 1)
            room_w_to = (room_temp['x']-1, room_temp['y'])

            room_temp['s_to'] = (room_temp['x'], room_temp['y'] - 1)
            room_temp['w_to'] = (room_temp['x']-1, room_temp['y'])

        # Top Left
        elif room_temp['x'] == min_coord:
            room_s_to = (room_temp['x'], room_temp['y'] - 1)
            room_e_to = (room_temp['x']+1, room_temp['y'])

            room_temp['s_to'] = (room_temp['x'], room_temp['y'] - 1)
            room_temp['e_to'] = (room_temp['x']+1, room_temp['y'])

        else:
            room_s_to = (room_temp['x'], room_temp['y'] - 1)
            room_e_to = (room_temp['x']+1, room_temp['y'])
            room_w_to = (room_temp['x']-1, room_temp['y'])

            room_temp['s_to'] = (room_temp['x'], room_temp['y'] - 1)
            room_temp['e_to'] = (room_temp['x']+1, room_temp['y'])
            room_temp['w_to'] = (room_temp['x']-1, room_temp['y'])

    # Bottom Edge
    elif room_temp['y'] == min_coord:

        # Bottom right
        if room_temp['x'] == max_coord:
            room_n_to = (room_temp['x'], room_temp['y'] + 1)
            room_w_to = (room_temp['x']-1, room_temp['y'])

            room_temp['n_to'] = (room_temp['x'], room_temp['y'] + 1)
            room_temp['w_to'] = (room_temp['x']-1, room_temp['y'])

        # Bottom Left
        elif room_temp['x'] == min_coord:
            room_n_to = (room_temp['x'], room_temp['y'] + 1)
            room_e_to = (room_temp['x']+1, room_temp['y'])

            room_temp['n_to'] = (room_temp['x'], room_temp['y'] + 1)
            room_temp['e_to'] = (room_temp['x']+1, room_temp['y'])

        else:
            room_n_to = (room_temp['x'], room_temp['y'] + 1)
            room_e_to = (room_temp['x']+1, room_temp['y'])
            room_w_to = (room_temp['x']-1, room_temp['y'])

            room_temp['n_to'] = (room_temp['x'], room_temp['y'] + 1)
            room_temp['e_to'] = (room_temp['x']+1, room_temp['y'])
            room_temp['w_to'] = (room_temp['x']-1, room_temp['y'])

    # everything without an edge
    else:
        room_s_to = (room_temp['x'], room_temp['y'] - 1)
        room_n_to = (room_temp['x'], room_temp['y'] + 1)
        room_w_to = (room_temp['x']-1, room_temp['y'])
        room_e_to = (room_temp['x']+1, room_temp['y'])

        room_temp['n_to'] = (room_temp['x'], room_temp['y'] + 1)
        room_temp['e_to'] = (room_temp['x']+1, room_temp['y'])
        room_temp['w_to'] = (room_temp['x']-1, room_temp['y'])
        room_temp['s_to'] = (room_temp['x'], room_temp['y'] - 1)

    all_rooms.append(room_temp)

# Chance the direction_to to room id's instead of coords
for room1 in all_rooms:
    for room2 in all_rooms:
        
        if room1['n_to'] != [] and type(room1['n_to']) != int:
            if -1 in room1['n_to']:
                room1['n_to'] = -1
            elif room2['x'] == room1['n_to'][0] and room2['y'] == room1['n_to'][1]:
                room1['n_to'] = room2['id']

        elif room1['n_to'] == []:
            room1['n_to'] = -1

        if room1['e_to'] != [] and type(room1['e_to']) != int:
            if -1 in room1['e_to']:
                room1['e_to'] = -1
            elif room2['x'] == room1['e_to'][0] and room2['y'] == room1['e_to'][1]:
                room1['e_to'] = room2['id']

        elif room1['e_to'] == []:
            room1['e_to'] = -1

        if room1['s_to'] != [] and type(room1['s_to']) != int:
            if -1 in room1['s_to']:
                room1['s_to'] = -1
            elif room2['x'] == room1['s_to'][0] and room2['y'] == room1['s_to'][1]:
                room1['s_to'] = room2['id']

        elif room1['s_to'] == []:
            room1['s_to'] = -1

        if room1['w_to'] != [] and type(room1['w_to']) != int:
            if -1 in room1['w_to']:
                room1['w_to'] = -1
            elif room2['x'] == room1['w_to'][0] and room2['y'] == room1['w_to'][1]:
                room1['w_to'] = room2['id']

        elif room1['w_to'] == []:
            room1['w_to'] = -1

# Add all the rooms to the db
for room in all_rooms:
    Room(id=room['id'], title=room['title'], description=room['desc'],
     x=room['x'], y=room['y'],
     n_to=room['n_to'],
     e_to=room['e_to'],
     s_to=room['s_to'],
     w_to=room['w_to']).save()
