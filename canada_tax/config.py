from django.utils.translation import ugettext_lazy as _
from livesettings import * 
from tax.config import TAX_MODULE

TAX_MODULE.add_choice(('canada_tax', _('Canadian Tax Module')))

TAX_GROUP = config_get_group('TAX')
        
config_register(
     BooleanValue(TAX_GROUP,
         'TAX_SHIPPING_CANADIAN',
         description=_("Tax Shipping?"),
         requires=TAX_MODULE,
         requiresvalue='canada_tax',
         default=False)
)

