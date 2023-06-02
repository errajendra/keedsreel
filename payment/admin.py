from django.contrib import admin
from .models import Transaction, UserSubscription
from talvido_app.admin import BaseModelAdmin


@admin.register(Transaction)
class TransactionAdmin(BaseModelAdmin):
    list_display = ["id", "name", "payment_id", "order_id"]


@admin.register(UserSubscription)
class UserSubscriptionAdmin(BaseModelAdmin):
    list_display = ["id", "name", "created_at", "subscription_end_date"]
