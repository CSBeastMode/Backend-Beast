from django.contrib.auth.models import User
from charlie.models import Player, Room

Room.objects.all().delete()

def create_rooms(n_rooms, seed=None):
    import random
    from util.classes import FakeRoom
    from charlie.models import Player, Room
    ##### FUNCTIONS #####

    # Given a coords and list/list of lists of rooms,
    # check if coords are in room
    def exists(coords: tuple, all_rooms):
        if all_rooms == []:
            return False

        flat_rooms = []
        if type(all_rooms[0]) == list:
            for i in all_rooms:
                for j in i:
                    flat_rooms.append((j.x, j.y))    
        else:
            for i in all_rooms:
                flat_rooms.append((i.x, i.y))

        if coords in flat_rooms:
                return True
            
        return False

    # Get room object based off coords
    def get_room(coords: tuple, rooms):
        for i in rooms:
            for j in i:
                if (j.x, j.y) == coords:
                    return j

    #####  END OF FUNCTIONS #####

    room_types = [
    ('Hallway', 'A corridor with red emergency lights illuminating the room and the occasional sparks from loose wires'),
    ('Crew Cabin', 'A crew members cabin with a small mattress and mementos'),
    ('Mess Hall', 'A large room with tables for eating, food is everwhere'),
    ('Recreation Center', 'A room with excercise equipment and foosball tables'),
    ('Bathroom', 'The cleanest bathroom you\'ve ever seen'),
    ('Medical Bay', 'Lot of medical supplies still around'),
    ('Weapons Room', 'Lots of locked up weapons'),
    ('Engineering Bay', 'Place of engineering')]

    # Instatiate rooms list
    rooms = [[Room(0, 'Engine Room', 'Room of Engine', 0, 0)]]

    # Keep count for room created for id
    counter = 1

    # If seed, use it
    if seed: 
        random.seed(seed)
    
    # Create rooms until we reach desired rooms
    while counter < n_rooms:

        # create a temp list to hold created rooms for each iteration
        temp = []

        # for each room created in last iteration, create rooms off of those points
        for i in rooms[-1]:
            n_paths = random.randint(1, 4) 
            for j in range(1, n_paths + 1):
                choice = random.choice(['n', 'e', 's', 'w'])
                room_type = random.choice(room_types)

                # Check if we can place a room in a direction, then do it or connect two rooms
                if choice == 'n' and i.n_to == None:
                    if exists((i.x, i.y + 1), rooms) == False and exists((i.x, i.y + 1), temp) == False:
                        placeholder = FakeRoom(id=counter, title=room_type[0], description=room_type[1], x=i.x, y=i.y + 1, s_to = i)
                        temp.append(placeholder)
                        i.n_to = placeholder
                        counter += 1
                    else:
                        i.n_to = get_room((i.x, i.y + 1), rooms)

                elif choice == 'e' and i.e_to == None:
                    if exists((i.x + 1, i.y), rooms) == False and exists((i.x + 1, i.y), temp) == False:
                        placeholder = FakeRoom(id=counter, title=room_type[0], description=room_type[1], x=i.x + 1, y=i.y, w_to = i)
                        temp.append(placeholder)
                        i.e_to = placeholder
                        counter += 1
                    else:
                        i.e_to = get_room((i.x + 1, i.y), rooms)

                elif choice == 's' and i.s_to == None:
                    if exists((i.x, i.y - 1), rooms) == False and exists((i.x, i.y - 1), temp) == False:
                        placeholder = FakeRoom(id=counter, title=room_type[0], description=room_type[1], x=i.x, y=i.y - 1, n_to = i)
                        i.s_to = placeholder
                        temp.append(placeholder)
                        counter += 1
                    else:
                        i.s_to = get_room((i.x, i.y - 1), rooms)

                elif choice == 'w' and i.w_to == None:
                    if exists((i.x - 1, i.y), rooms) == False and exists((i.x - 1, i.y), temp) == False:
                        placeholder = FakeRoom(id=counter, title=room_type[0], description=room_type[1], x=i.x - 1, y=i.y, e_to = i)
                        temp.append(placeholder)
                        i.w_to = placeholder
                        counter += 1
                    else:
                        i.w_to = get_room((i.x - 1, i.y), rooms)

                else:
                    continue

        # if rooms were created, append list of rooms to room list
        if temp != []:
            rooms.append(temp)

    # return the rooms created as 1D list
    return_rooms = []
    for i in rooms:
        for j in i:
            return_rooms.append(j)

    return return_rooms


prep_rooms = create_rooms(500)

# Add all the rooms to the db

for room in prep_rooms:
    if room.n_to != None:
        room.n_to = room.n_to.id

    if room.e_to != None:
        room.e_to = room.e_to.id

    if room.s_to != None:
        room.s_to = room.s_to.id

    if room.w_to != None:
        room.w_to = room.w_to.id

    Room(id=room.id, title=room.title, description=room.description, x=room.x, y=room.y, n_to=room.n_to, e_to=room.e_to, s_to=room.s_to, w_to=room.w_to).save()