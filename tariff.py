#!/usr/bin/python
# License: WTFPL
# http://sam.zoy.org/wtfpl/

from __future__ import division
import sys
from tariffs import tariffs

IVA = 0.18
MINUTES = 60
ESTABLISHMENT = 0.15

def printTariff():
    tariff = sys.argv[2]
    fdata = open(sys.argv[1])
    mtariff = tariffs[tariff]['minutes'] # 0.022 - 0.027
    dtariff = tariffs[tariff]['data']
    total = 0
    
    for line in fdata.readlines():
        line = line.replace('\n','')
        (mins, secs) = line.split(':')
        minutes = int(mins) + (int(secs)/MINUTES)
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


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print >> sys.stderr, "usage: %s file tariff" % sys.argv[0]
        exit(-1)
    printTariff()
