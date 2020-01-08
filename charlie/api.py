from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    # if direction == "n":
    #     nextRoomID = room.n_to
    # elif direction == "s":
    #     nextRoomID = room.s_to
    # elif direction == "e":
    #     nextRoomID = room.e_to
    # elif direction == "w":
    #     nextRoomID = room.w_to
    ######### Testing with current iteration ##########
    if direction == "n":
        nextRoomX = room.n_to_x
        nextRoomY = room.n_to_y
        for tile in Room.objects.all():
            if nextRoomX == tile.coord_x and nextRoomY == tile.coord_y:
                nextRoomID = tile.id
        # xResult = Room.objects.filter(coord_x=nextRoomX)
        # print(f'\nxResult: {xResult}')
        # yResult = xResult.filter(coord_y=nextRoomY)
        # print(f'\nyResult: {yResult}')
        # nextRoom = Room.objects.filter(coord_x=nextRoomX).get(coord_y=nextRoomY)
        # if nextRoom is None:
        #     pass
        # print(f'\n{nextRoom}')
        # nextRoomID = nextRoom.id
        # print(f'\n{nextRoomID}')
    elif direction == "s":
        nextRoomX = room.s_to_x
        nextRoomY = room.s_to_y
        for tile in Room.objects.all():
            if nextRoomX == tile.coord_x and nextRoomY == tile.coord_y:
                nextRoomID = tile.id
    elif direction == "e":
        nextRoomX = room.e_to_x
        nextRoomY = room.e_to_y
        for tile in Room.objects.all():
            if nextRoomX == tile.coord_x and nextRoomY == tile.coord_y:
                nextRoomID = tile.id
    elif direction == "w":
        nextRoomX = room.w_to_x
        nextRoomY = room.w_to_y
        for tile in Room.objects.all():
            if nextRoomX == tile.coord_x and nextRoomY == tile.coord_y:
                nextRoomID = tile.id
    ##########
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom=nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)