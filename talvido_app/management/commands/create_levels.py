from django.core.management.base import BaseCommand
from mlm.models import Level


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for i in range(0,7):
            Level.objects.create(
                level = i+1,
                referral_users = int(str(10) + str(str(0)*i))
            )
        print("done !!")
