from app.repo.base import BaseRepo
from app.users.models import Users



class UserRepo(BaseRepo):
    model = Users
