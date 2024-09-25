from django.contrib import admin
from .models import Norm

@admin.register(Norm)
class NormAdmin(admin.ModelAdmin):
    list_display = ('no', 'description', 'unit_price', 'vat_print', 'vat_download', 'stock_status', 'status')
    search_fields = ('no', 'description', 'dok_nr')
