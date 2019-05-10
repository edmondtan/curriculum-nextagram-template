from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property
import peewee as pw
from config import S3_LOCATION

class ProfilePage(BaseModel):
    user_id = pw.ForeignKeyField(User)
    posted_image = pw.CharField(null=True)

    @hybrid_property
    def profile_picture_url(self):
        return f'{S3_LOCATION}{self.posted_image}'
