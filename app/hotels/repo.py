from app.hotels.models import Hotels
from app.repo.base import BaseRepo


class HotelsRepo(BaseRepo):
    model = Hotels
