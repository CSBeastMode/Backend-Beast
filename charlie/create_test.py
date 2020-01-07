from models import Room
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beastmode.settings')

random_room = Room(title='A random room', description='Very randomness')
random_room.save()