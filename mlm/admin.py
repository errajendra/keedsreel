from django.contrib import admin
from .models import Level, WalletHistory


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ["id", "level", "referral_users"]


@admin.register(WalletHistory)
class WalletHistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "amount", "date"]
