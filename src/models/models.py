import peewee

db = peewee.SqliteDatabase('res/database.db')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Users(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    user_id = peewee.IntegerField(unique=True)
    username = peewee.CharField(unique=True, null=True)
    admin_title = peewee.CharField(null=True)


class Roles(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField(unique=True)
    users = peewee.ManyToManyField(Users, backref='roles')


class UserStatistics(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    user_id = peewee.CharField(unique=True)
    username = peewee.CharField(unique=True, null=True)
    message_count = peewee.IntegerField(null=True)
    rofl_count = peewee.IntegerField(null=True)


UserRoles = Roles.users.get_through_model()
