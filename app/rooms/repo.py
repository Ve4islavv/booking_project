from app.repo.base import BaseRepo
from app.rooms.models import Rooms


class RoomsRepo(BaseRepo):
    model = Rooms

