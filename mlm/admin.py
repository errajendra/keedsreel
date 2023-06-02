from django.contrib import admin
from .models import Level, WalletHistory
from talvido_app.admin import BaseModelAdmin


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ["id", "level", "referral_team", "users", "daily_income"]


@admin.register(WalletHistory)
class WalletHistoryAdmin(BaseModelAdmin):
    list_display = ["id", "user", "name", "amount", "date"]
