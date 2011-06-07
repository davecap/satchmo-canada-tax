Django app to manage Canadian taxes in Satchmo.

Adapted from the version created by Benoit C. Sirois:
http://bitbucket.org/benoitcsirois/satchmo-canada-tax

You need to add the CanadianTaxRate model and then add the following data to it in the Django admin:

Tax Class, Tax Zone, Tax Country, Display percentage, Enter your tax number here

Default Ontario                     None    13.00%  HST 13%
Default Newfoundland and Labrador   None    13.00%  HST 13%
Default New Brunswick               None    13.00%  HST 13%
Default British Columbia            None    12.00%  HST 12%
Default Quebec                      None    8.50%   QST 8.5%
Default None                        Canada  5.00%   GST 5%

Make sure you set the compound order appropriately. Now you can apply tax to products shipped to Quebec (GST and QST) and apply GST only to those shipped to Canada.

Note: If you want to tax shipping costs then you will probably have to modify some code.
