from django.contrib.auth.models import User
from charlie.models import Player, Room
from itertools import product
import random
import copy
import uuid

Room.objects.all().delete()

high_prob_rooms = [
    ('Hallway', 'An empty corridor'),
    ('Crew Cabin', 'Bedroom')
]

med_prob_rooms = [
    ('Mess Hall', 'Place of eating'),
    ('Recreation Center', 'Place of fun'),
    ('Bathroom', 'Place of pooping')  
]

low_prob_rooms = [
    ('Medical Bay', 'Place of healing'),
    ('Weapons', 'Defense Systems'),
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
for i in range(100):
    room = ('None', 'None')
    cord = (-1, -1)
    room_n_to = (-1, -1)
    room_e_to = (-1, -1)
    room_s_to = (-1, -1)
    room_w_to = (-1, -1)


    room_prob = random.randint(1, 100)

    if i == 0:
        cord = (0, 0)
        coordinates.remove(cord)

        room = single_rooms[0]
        single_rooms.remove(room)

        room_coords = cord

    elif i == 1:
        cord = (1, 8)
        coordinates.remove(cord)

        room = single_rooms[0]
        single_rooms.remove(room)

        room_coords = cord

    elif i == 2:
        cord = (3, 6)
        coordinates.remove(cord)

        room = single_rooms[0]
        single_rooms.remove(room)

        room_coords = cord

    elif i == 3:
        cord = (7, 2)
        coordinates.remove(cord)

        room = single_rooms[0]
        single_rooms.remove(room)

        room_coords = cord

    elif i == 4:
        cord = (9, 9)
        coordinates.remove(cord)

        room = single_rooms[0]
        single_rooms.remove(room)

        room_coords = cord

    else:
        cord = random.choice(coordinates)
        coordinates.remove(cord)

        if room_prob < 60:
            room = random.choice(high_prob_rooms)
            room_coords = cord

        elif room_prob > 59 and room_prob < 90:
            room = random.choice(med_prob_rooms)
            room_coords = cord

        else:
            room = random.choice(low_prob_rooms)
            room_coords = cord

    # Left edge
    if room_coords[0] == min_coord:

        # left, bottom corner x,y = 0
        if room_coords[1] == min_coord:
            room_n_to = (room_coords[0], room_coords[1] + 1)
            room_e_to = (room_coords[0]+1, room_coords[1])

        # left top corner, x=0, y=max
        if room_coords[1] == max_coord:
            room_s_to = (room_coords[0], room_coords[1] - 1)
            room_e_to = (room_coords[0]+1, room_coords[1])

        # far left middle
        else:
            room_n_to = (room_coords[0], room_coords[1] + 1)
            room_s_to = (room_coords[0], room_coords[1] - 1)
            room_e_to = (room_coords[0]+1, room_coords[1])

    # Right edge
    elif room_coords[0] == max_coord:

        # right bottom corner
        if room_coords[1] == min_coord:
            room_n_to = (room_coords[0], room_coords[1] + 1)
            room_w_to = (room_coords[0]-1, room_coords[1])

    # right top corner
        if room_coords[1] == max_coord:
            room_s_to = (room_coords[0], room_coords[1] - 1)
            room_w_to = (room_coords[0]-1, room_coords[1])

    # far right middle
        else:
            room_n_to = (room_coords[0], room_coords[1] + 1)
            room_s_to = (room_coords[0], room_coords[1] - 1)
            room_w_to = (room_coords[0]-1, room_coords[1])

    # Top edge
    elif room_coords[1] == max_coord:
        
        # Top right
        if room_coords[0] == max_coord:
            room_s_to = (room_coords[0], room_coords[1] - 1)
            room_w_to = (room_coords[0]-1, room_coords[1])
        
        # Top Left
        elif room_coords[0] == min_coord:
            room_s_to = (room_coords[0], room_coords[1] - 1)
            room_e_to = (room_coords[0]+1, room_coords[1])

        else:
            room_s_to = (room_coords[0], room_coords[1] - 1)
            room_e_to = (room_coords[0]+1, room_coords[1])
            room_w_to = (room_coords[0]-1, room_coords[1])

    # Bottom Edge
    elif room_coords[1] == min_coord:
        
        # Bottom right
        if room_coords[0] == max_coord:
            room_n_to = (room_coords[0], room_coords[1] + 1)
            room_w_to = (room_coords[0]-1, room_coords[1])
        
        # Bottom Left
        elif room_coords[0] == min_coord:
            room_n_to = (room_coords[0], room_coords[1] + 1)
            room_e_to = (room_coords[0]+1, room_coords[1])

        else:
            room_n_to = (room_coords[0], room_coords[1] + 1)
            room_e_to = (room_coords[0]+1, room_coords[1])
            room_w_to = (room_coords[0]-1, room_coords[1])

    # everything without an edge
    else:
        room_s_to = (room_coords[0], room_coords[1] - 1)
        room_n_to = (room_coords[0], room_coords[1] + 1)
        room_w_to = (room_coords[0]-1, room_coords[1])
        room_e_to = (room_coords[0]+1, room_coords[1])

    Room(id=uuid.uuid4(), title=room[0], description=room[1], coord_x=cord[0], coord_y=cord[1],
     n_to_x=room_n_to[0], n_to_y=room_n_to[1],
     e_to_x=room_e_to[0], e_to_y=room_e_to[1],
     s_to_x=room_s_to[0], s_to_y=room_s_to[1],
     w_to_x=room_w_to[0], w_to_y=room_w_to[1]).save()
