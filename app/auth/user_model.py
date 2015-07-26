import logging
log = logging.getLogger()

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app.database import (
    BaseModel,
    CharField, DateTimeField, BooleanField
)

from app.identifier import Identifier


class EmailExistsException(Exception):
    pass

class EmailNotVerifiedException(Exception):
    pass

class InvalidPasswordException(Exception):
    pass


class User(BaseModel):

    join_date = DateTimeField()

    name = CharField()
    email = CharField(unique=True)
    password = CharField()
    
    email_validated = BooleanField()
    email_validation_secret = CharField(null=True, unique=True)

    recovery_requested = BooleanField()
    recovery_date = DateTimeField(null=True)
    recovery_secret = DateTimeField(null=True)
    

    @classmethod
    def create_from_registration(cls, name, email, password):
        user = cls.select().where(cls.email == email)
        if user.exists():
            raise EmailExistsException('account with given email already exists')
        return cls.create(
            join_date=datetime.utcnow(),
            name=name,
            email=email,
            password=generate_password_hash(password),
            email_validated=False,
            email_validation_secret=str(Identifier.new_random()),
            recovery_requested=False
        )

    @classmethod
    def login(cls, email, password):
        user = cls.select().where(cls.email == email)
        if not user.exists():
            raise InvalidPasswordException('no account with this email')
        user = user.get()
        if not user.email_validated:
            raise EmailNotVerifiedException('email not verified')
        if check_password_hash(user.password, password):
            return user
        else:
            raise InvalidPasswordException('password invalid')

    
