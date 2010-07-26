from decimal import Decimal
from django.utils.translation import ugettext as _
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from l10n.models import AdminArea, Country
from livesettings import config_value
from canada_tax.models import CanadianTaxRate as TaxRate
from product.models import TaxClass
from satchmo_store.contact.models import Contact
from satchmo_utils import is_string_like
import logging
import operator

log = logging.getLogger('tax.canada_tax')

class Processor(object):
    
    method = "area"
    
    def __init__(self, order=None, user=None):
        """
        Any preprocessing steps should go here
        For instance, copying the shipping and billing areas
        """
        self.order = order
        self.user = user
        
    def _get_location(self):
        area = None
        country = None
        
        calc_by_ship_address = bool(config_value('TAX','TAX_AREA_ADDRESS') == 'ship')
        
        if self.order:
            if calc_by_ship_address:
                country = self.order.ship_country
                area = self.order.ship_state
            else:
                country = self.order.bill_country
                area = self.order.bill_state
        
            if country:
                try:
                    country = Country.objects.get(iso2_code__exact=country)
                except Country.DoesNotExist:
                    log.error("Couldn't find Country from string: %s", country)
                    country = None
        elif self.user and self.user.is_authenticated():
            try:
                contact = Contact.objects.get(user=self.user)
                try:
                    if calc_by_ship_address:
                        area = contact.shipping_address.state
                    else:
                        area = contact.billing_address.state
                except AttributeError:
                    pass
                try:
                    if calc_by_ship_address:
                        country = contact.shipping_address.country
                    else:
                        country = contact.billing_address.country
                except AttributeError:
                    pass
            except Contact.DoesNotExist:
                pass

        if not country:
            from satchmo_store.shop.models import Config
            country = Config.objects.get_current().sales_country

        if area:
            try:
                area = AdminArea.objects.get(name__iexact=area,
                                             country=country)
            except AdminArea.DoesNotExist:
                try:
                    area = AdminArea.objects.get(abbrev__iexact=area,
                                                 country=country)
                except AdminArea.DoesNotExist:
                    log.info("Couldn't find AdminArea from string: %s", area)
                    area = None
        return area, country
    
    # taxclass: string, Default, Shipping
    # area: state/province
    # country: country!
    # get_object: return the rate object(s)
    def get_rate(self, taxclass=None, area=None, country=None, get_object=False, **kwargs):
        if not taxclass:
            taxclass = "Default"
        
        # initialize the rates array, allow for more than one rate
        rates = []
        
        # get the area/country
        if not (area or country):
            area, country = self._get_location()

        # get the taxclass object
        if is_string_like(taxclass):
            try:
                taxclass = TaxClass.objects.get(title__iexact=taxclass)
            except TaxClass.DoesNotExist:
                raise ImproperlyConfigured("Can't find a '%s' Tax Class", taxclass)
        
        # get all the rates for the given area
        if area:
            try:
                rates += list(TaxRate.objects.filter(taxClass=taxclass, taxZone=area))
            except TaxRate.DoesNotExist:
                pass
        
        # get all rates for the given country
        if country:
            try:
                rates += list(TaxRate.objects.filter(taxClass=taxclass, taxCountry=country))
            except TaxRate.DoesNotExist:
                pass

        log.debug("Got rates for taxclass: %s, area: %s, country: %s = [%s]", taxclass, area, country, rates)

        if get_object:
            return self.tax_rate_list(rates)
        else:
            return self.tax_rate_list(rates)[0]

    def get_percent(self, taxclass="Default", area=None, country=None):
        return 100*self.get_rate(taxclass=taxclass, area=area, country=country)
    
    # given a list of TaxRate objects
    #   - try to split into compounded/non-compounded rates
    #   - order the compound rates properly
    #   - finalize all the rates such that the sum of each rate*price is the total tax
    #   - return total tax rate + list of taxCodes and individual rates
    #       (decimal('X,XX'), [('TAXCODE', Decimal('X.XX'))]
    def tax_rate_list(self, rates):
        if len(rates) == 0:
            return (Decimal("0.00"), [])
        
        override_rates = filter(lambda x: x.override == True, rates)
        if len(override_rates):
            # since this is a single overriding rate, it returns the first
            # override rate found, along with related rate data.
            return (percentage, [(override_rates[0].taxCode, override_rates[0].percentage)])

        regular_rates = filter(lambda x: x.compound == False, rates)
        compound_rates = sorted(filter(lambda x: x.compound == True, rates), key=operator.attrgetter("compound_order"))
        
        totalrate = Decimal('0.00')
        receipt_data = []

        # adding / compounding tax rates
        for rate in regular_rates:
            receipt_data.append((rate.taxCode, rate.percentage))
            totalrate += rate.percentage
            
        for rate in compound_rates:
            percentage = rate.percentage + (rate.percentage * totalrate)
            receipt_data.append((rate.taxCode, percentage))
            totalrate += percentage
        
        return (totalrate, receipt_data)

    def by_price(self, taxclass, price):
        rate = self.get_rate(taxclass)
        return rate * price

    def by_product(self, product, quantity=Decimal('1')):
        """Get the tax for a given product"""
        price = product.get_qty_price(quantity)[0]
        tc = product.taxClass
        return self.by_price(tc, price)
        
    def by_orderitem(self, orderitem):
        if orderitem.product.taxable:
            price = orderitem.sub_total
            taxclass = orderitem.product.taxClass
            return self.by_price(taxclass, price)
        else:
            return Decimal("0.00")

    def shipping(self, subtotal=None):
        if subtotal is None and self.order:
            subtotal = self.order.shipping_sub_total

        if subtotal:
            rate = None
            if config_value('TAX','TAX_SHIPPING_CANADIAN'):
                try:
                    # get the tax class used for taxing shipping
                    tc = TaxClass.objects.get(title=config_value('TAX', 'TAX_CLASS'))
                    rate = self.get_rate(taxclass=tc)
                    return rate * subtotal
                except:
                    log.error("'Shipping' TaxClass doesn't exist.")
        return Decimal("0.00")

    def process(self, order=None):
        """
        Calculate the tax and return it.
        """
        if order:
            self.order = order
        else:
            order = self.order
        
        sub_total = Decimal('0.00')
        tax_details = {}
        
        rates = {}
        for item in order.orderitem_set.filter(product__taxable=True):
            tc = item.product.taxClass
            if tc:
                tc_key = tc.title
            else:
                tc_key = "Default"
            if rates.has_key(tc_key):
                rate = rates[tc_key]
            else:
                rate, taxes = self.get_rate(tc, get_object=True)
                for r in taxes:
                    tax_details[r[0]] = Decimal('0.00')
                rates[tc_key] = rate
                
            price = item.sub_total
            sub_total += price*rate
            for r in taxes:
                tax_details[r[0]] += r[1]*price
        
        #shipping_tax = self.shipping()
        #$sub_total += shipping_tax
        #tax_details[_('Tax on Shipping')] = shipping_tax
        
        return sub_total, tax_details
