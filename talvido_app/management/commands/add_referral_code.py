from django.core.management.base import BaseCommand
from talvido_app.models import Talvidouser
from django.utils.crypto import get_random_string
from django.db.models import F


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        users = Talvidouser.objects.all()
        for user in users:
            user.referral_code = get_random_string(5).upper()
            user.save()
            print("Added Referral_code of " +  user.firebase_uid)
