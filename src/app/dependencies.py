from src.app import service
from src.app.exceptions import UsernameTaken
from src.app.schemas import User


async def valid_user_create(user: User) -> User:
    if await service.get_user_by_username(user.username):
        raise UsernameTaken()

    return user
