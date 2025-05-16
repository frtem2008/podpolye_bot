import logging

from src import logsetup
from src.models import models
from src.models.models import db, Users, Roles, UserRoles, UserStatistics

logger = logsetup.new_logger('Database', logging.INFO)


def init_db():
    logger.warning("Set working directory to project root for database to work!")
    db.connect()
    db.create_tables([models.Users, models.Roles, models.UserRoles, models.UserStatistics], safe=True)
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


def count_mes_pl(user_id: int):
    user = UserStatistics.get(id=user_id)
    user.count_messege = 1 + user.count_messege1
    user.save()


def count_goida_pl(user_id: int):
    user = UserStatistics.get(id=user_id)
    user.count_goida = 1 + user.count_goida
    user.save()


def get_statistics():
    return UserStatistics.select()


def create_user_statistics(user_id: int, username: str):
    return UserStatistics.create(id=user_id, count_messege=0, count_goida=0, username=username)



