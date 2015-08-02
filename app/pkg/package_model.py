import logging
log = logging.getLogger()

from app.database import (
    BaseModel,
    CharField, DateTimeField, BooleanField, IntegerField,
)




class Package(BaseModel):
    name = CharField(unique=True)
    description = CharField()
    sha1 = CharField()
    pkgtype = CharField()
    version = CharField()
    patchlevel = IntegerField()
    filename = CharField()
    

    def to_json(self):
        return dict(
            name=self.name,
            description=self.description,
            sha1=self.sha1,
            pkgtype=self.pkgtype,
            version=self.version,
            patchlevel=self.patchlevel,
            filename=self.filename,
        )
            
    
