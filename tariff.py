#!/usr/bin/python
# License: WTFPL
# http://sam.zoy.org/wtfpl/

from __future__ import division
import sys

IVA = 0.18
MINUTES = 60
ESTABLISHMENT = 0.15

tariff = sys.argv[2]
tariffs = {'elefantito' : {'minutes' : 0.027, 'data': 6.9},
           'lobo' : {'minutes' : 0.022, 'data': 8.5} }

fdata = open(sys.argv[1])
mtariff = tariffs[tariff]['minutes'] # 0.022 - 0.027
dtariff = tariffs[tariff]['data']
total = 0

for line in fdata.readlines():
    line = line.replace('\n','')
    minutes = int(line.split(':')[0]) + (int(line.split(':')[1])/MINUTES)
    cost = (minutes * mtariff) + ESTABLISHMENT    
    print "%s - %s" % (line, cost)
    total += cost
    
print "calls: %s" % total
total += dtariff
print "calls + %s data plan : %s" % (dtariff, total)
vat = total*IVA
total += vat
print "VAT: %s" % vat
print "TOTAL: %s" % total
