import logging

from src import logsetup
from src.models import models
from src.models.models import db, Users, Roles, UserRoles

logger = logsetup.new_logger('Database', logging.INFO)


def init_db() -> None:
    logger.warning("Set working directory to project root for database to work!")
    db.connect()
    db.create_tables([models.Users, models.Roles, models.UserRoles], safe=True)
    logger.info('Database initialized')


def create_user(user_id: int, username: str, admin_title: str) -> Users:
    return Users.create(user_id=user_id, username=username, admin_title=admin_title)


def create_role(name: str) -> Roles:
    return Roles.create(name=name)


def get_users() -> list[Users]:
    return list(Users.select())


def get_user(username: str) -> Users | None:
    return Users.get_or_none(username=username)


def get_role(name: str) -> Roles | None:
    return Roles.get_or_none(name=name)


def get_role_names() -> list[str]:
    return [role.name for role in Roles.select()]


def get_user_role_names(user_id: int) -> list[str]:
    return [role.name for role in Users.get(user_id=user_id).roles]


def get_role_users(role: str) -> list[Users]:
    return [user for user in Roles.get(name=role).users]


def update_user(user_id: int, username: str, admin_title: str) -> Users:
    return Users.update(user_id=user_id, username=username, admin_title=admin_title)


def give_role(user_id: int, role: str) -> Roles:
    return Users.get(user_id=user_id).roles.add(Roles.get(name=role))


def remove_role(user_id: int, role: str) -> Roles:
    return Users.get(user_id=user_id).roles.remove(Roles.get(name=role))


def delete_role(role: str) -> None:
    UserRoles.delete().where((UserRoles.roles_id == Roles.get(name=role))).execute()
    Roles.get(name=role).delete_instance()
