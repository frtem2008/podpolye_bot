import logging

from src import logsetup
from src.models import models
from src.models.models import db, Users, Roles, UserRoles

logger = logsetup.new_logger('Database', logging.INFO)


def init_db():
    db.connect()
    db.create_tables([models.Users, models.Roles, models.UserRoles], safe=True)
    logger.info('Database initialized')


def create_user(user_id: int, username: str, admin_title: str):
    return Users.create(user_id=user_id, username=username, admin_title=admin_title)


def create_role(name: str):
    return Roles.create(name=name)


def get_users():
    return list(Users.select())


def get_user(username: str):
    return Users.get_or_none(username=username)


def get_role(name: str):
    return Roles.get_or_none(name=name)


def get_roles():
    return map(lambda role: role.name, list(Roles.select()))


def get_user_roles(user_id: int):
    return [role.name for role in Users.get(user_id=user_id).roles]


def get_role_users(role: str):
    return [user for user in Roles.get(name=role).users]


def update_user(user_id: int, username: str, admin_title: str):
    return Users.update(user_id=user_id, username=username, admin_title=admin_title)


def give_role(user_id: int, role: str):
    return Users.get(user_id=user_id).roles.add(Roles.get(name=role))


def remove_role(user_id: int, role: str):
    return Users.get(user_id=user_id).roles.remove(Roles.get(name=role))


def delete_role(role: str):
    UserRoles.delete().where((UserRoles.roles_id == Roles.get(name=role))).execute()
    Roles.get(name=role).delete_instance()
