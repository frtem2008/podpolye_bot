import logging

from src import log_setup
from src.database import models
from src.database.models import db, Users, Roles

logger = log_setup.new_logger('Database', logging.INFO)

def init_db():
    db.connect()
    with db:
        db.create_tables([models.Users, models.Roles], safe=True)
    logger.info('Database initialized')


def add_user(user_id: int, username: str, admin_title: str):
    return Users.create(user_id=user_id, username=username, admin_title=admin_title)

def add_role(role_name:str):
    return Roles.create(role_name=role_name)

def update_user(user_id: int, username: str, admin_title: str):
    return Users.update(user_id=user_id, username=username, admin_title=admin_title)

def get_users():
    return list(Users.select())


def get_roles():
    return list(Roles.select())
