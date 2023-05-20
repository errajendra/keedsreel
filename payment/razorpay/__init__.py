import razorpay
from django.conf import settings


client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

client.set_app_details({"title" : "Talvido", "version" : "4.2"})
