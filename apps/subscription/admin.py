from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id','subscription_nr', 'subscription_code', 'customer', 'date_start', 'date_end', 'active')
    search_fields = ('subscription_nr', 'subscription_code', 'customer__name')
    list_filter = ('active', 'subscription_code', 'subscription_type')
