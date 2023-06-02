from django.contrib import admin
from .models import Transaction, UserSubscription


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "payment_id", "order_id"]


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at", "subscription_end_date"]

    def name(self, instance):
        return instance.user.first_name + " " + instance.user.last_name
