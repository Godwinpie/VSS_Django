from django.contrib import admin
from .models import Firm, FirmPerson

@admin.register(Firm)
class FirmAdmin(admin.ModelAdmin):
    list_display = ('id', 'firm_no', 'name', 'customer_no')
    search_fields = ('name','firm_no', 'person_no', 'name')

@admin.register(FirmPerson)
class FirmPersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'firm_no', 'person_no', 'name')
    search_fields = ('name','firm_no', 'person_no', 'name')