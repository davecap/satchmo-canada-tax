from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from product.models import TaxClass
from tax.modules.area.models import TaxRate

class CanadianTaxRate(TaxRate):
    compound = models.BooleanField(_('Compound Tax'))
    override = models.BooleanField(_('Override National Tax (HST for example)'))
    compound_order = models.IntegerField(_('Compound Order'), null=True, blank=True)
    taxCode = models.CharField(_('Enter your tax number here'), max_length=255, null=True, blank=True)

import config

