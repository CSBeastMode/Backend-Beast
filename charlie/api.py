from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    xCoord = room.x
    yCoord = room.y
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'title':room.title, 'description':room.description, 'x_coord':xCoord, 'y_coord':yCoord, 'players':players}, safe=True)


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
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        xCoord = nextRoom.x
        yCoord = nextRoom.y
        player.currentRoom=nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        for p_uuid in currentPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'movement', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        for p_uuid in nextPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'movement', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'x_coord':xCoord, 'y_coord':yCoord, 'players':players, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'x_coord':room.x, 'y_coord':room.y, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


# Chat within the room
@csrf_exempt
@api_view(["POST"])
def say(request):
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    message = data['message']
    room = player.room()
    currentPlayerUUIDs = room.playerUUIDs(player_id)
    for p_uuid in currentPlayerUUIDs:
        pusher.trigger(f'p-channel-{p_uuid}', u'say', {f'{player.user.username}':f'{message}'})
    # send to self as well
    pusher.trigger(f'p-channel-{player_uuid}', u'say', {f'{player.user.username}':f'{message}'})
    return JsonResponse({'name':player.user.username, 'message':message, 'chat_type':"say", 'error_msg':""}, safe=True)


# Broadcast to all players
@csrf_exempt
@api_view(["POST"])
def shout(request):
    player = request.user.player
    data = json.loads(request.body)
    message = data['message']
    allPlayers = Player.objects.all()
    for person in allPlayers:
        pusher.trigger(f'p-channel-{person.uuid}', u'shout', {f'{player.user.username} shouts':f'{message}'})
    return JsonResponse({'name':player.user.username, 'message':message, 'chat_type':"shout", 'error_msg':""}, safe=True)


# Whisper to single person
@csrf_exempt
@api_view(["POST"])
def whisper(request):
    player = request.user.player
    player_uuid = player.uuid
    data = json.loads(request.body)
    message = data['message']
    recipientName = data['to']
    # we need to grab the user object first
    user = User.objects.filter(username=recipientName).first()
    if user is not None:
        # user object allows us to grab the creation id to grab the player object
        recipient = Player.objects.get(user=user.id)
        pusher.trigger(f'p-channel-{recipient.uuid}', u'whisper', {f'{player.user.username} whispers':f'{message}'})
        # send to self as well
        pusher.trigger(f'p-channel-{player_uuid}', u'whisper', {f'Whisper to {recipient.user}':f'{message}'})
        return JsonResponse({'name':player.user.username, 'message':message, 'to':recipientName, 'chat_type':"whisper", 'error_msg':""}, safe=True)
    else:
        pusher.trigger(f'p-channel-{player.uuid}', u'error', {'Error':f'{recipientName} does not exist.'})
        return JsonResponse({'name':player.user.username, 'message':message, 'to':recipientName, 'chat_type':"whisper", 'error_msg':f"{recipientName} does not exist."}, safe=True, status=404)