from app import login_manager
from app.models import User
from flask import current_app

@login_manager.user_loader
def load_user(id):
    """

    :param id: username
    :return: return User object or None
    """
    current_app.logger.info(f'load_user: {id}')

    users = current_app.config['USERS']
    for user in users:
        if user[0] == id:
            return User(user[0],user[1])

    return None


