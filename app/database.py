
import peewee
from peewee import (
    SqliteDatabase,
    CharField, DateTimeField, BooleanField,
)
from app.config import config



database = SqliteDatabase(config.database)


class BaseModel(peewee.Model):
    class Meta:
        database = database


        
def all_database_models():
    from app.auth.user_model import User
    return [User]
