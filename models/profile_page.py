from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property
import peewee as pw
from config import S3_LOCATION
from peewee import fn

class ProfilePage(BaseModel):
    user = pw.ForeignKeyField(User, backref="images")
    posted_image = pw.CharField(null=True)
    caption = pw.CharField(null=True)

    @hybrid_property
    def profile_picture_url(self):
        return f'{S3_LOCATION}{self.posted_image}'

    # @hybrid_property
    # def total_donations(self):
    #     from models.donation import Donation
    #     total_donations = Donation.select(fn.SUM(Donation.amount).alias('total'), fn.COUNT(Donation.amount).alias('donation_count')).where(
    #         Donation.image_id == self.id)
    #     if total_donations[0].total == 0:
    #         return 0
    #     return str(round(total_donations[0].total, 2))
