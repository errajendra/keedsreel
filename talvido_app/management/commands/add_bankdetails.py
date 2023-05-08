from django.core.management.base import BaseCommand
from talvido_app.models import Talvidouser, BankDetail


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        users = Talvidouser.objects.all()
        try:
            BankDetail.objects.bulk_create(
                [BankDetail(user = user ) for user in users]
            )
            print("All bank details added !!")
        except:
            print("Already There !!")
