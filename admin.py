from django.contrib import admin
from canada_tax.models import CanadianTaxRate as TaxRate
from tax.modules.area.admin import TaxRateForm

class TaxRateOptions(admin.ModelAdmin):
    list_display = ("taxClass", "taxZone", "taxCountry", "display_percentage", "taxCode")
    form = TaxRateForm
    
admin.site.register(TaxRate, TaxRateOptions)

