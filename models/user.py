from models.base_model import BaseModel
import peewee as pw
from playhouse.hybrid import hybrid_property
from config import S3_LOCATION

class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=False)
    profile_image = pw.CharField(null=True)
    # private = pw.BooleanField(default=False)

    def is_authenticated():
        return True

    @hybrid_property
    def profile_image_url(self):
        return f'{S3_LOCATION}{self.profile_image}'

    # @hybrid_property
    # def is_private(self):
    #     return True if self.private else False