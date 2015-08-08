

from app.database import (
    BaseModel,
    CharField, DateTimeField, BooleanField
)



class KnownEmail(BaseModel):

    email = CharField(unique=True)
    """
    Email that is "known" and can be used to create a new account
    """











def update_known_emails(emails):
    for email in emails:
        KnownEmail.create(email=email)
        #known_email = KnownEmail.select().where(KnownEmail.email == email)
        #if not known_email.exists():
    
    
