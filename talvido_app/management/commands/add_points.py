from django.core.management.base import BaseCommand
from talvido_app.models import Talvidouser, Point


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        users = Talvidouser.objects.all()
        try:
            Point.objects.bulk_create(
                [Point(user = user, points=50 ) for user in users]
            )
            print("All points added !!")
        except:
            print("Already There !!")
