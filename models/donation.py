import peewee as pw
from models.user import User
from models.profile_page import ProfilePage
from models.base_model import BaseModel

class Donation(BaseModel):
    user = pw.ForeignKeyField(User, backref="donations")
    image = pw.ForeignKeyField(ProfilePage, backref="donations")
    amount = pw.DecimalField(decimal_places=2, null=False)