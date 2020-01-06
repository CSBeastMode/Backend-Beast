from models import Room
from django.contrib.auth.models import User

random_room = Room(title='A random room', description='Very randomness')
random_room.save()