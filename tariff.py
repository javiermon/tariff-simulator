#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- mode:python ; tab-width:4 -*- ex:set tabstop=4 shiftwidth=4 expandtab: -*-
# License: WTFPL
# http://sam.zoy.org/wtfpl/

from __future__ import division
import sys, re
from tariffs import tariffs

IVA = 0.18
MINUTES = 60
ESTABLISHMENT = 0.15

parser = re.compile(r"(?:(\d{2}):)?(\d{2}):(\d{2})")
evaluator = lambda x: 0 if x is None else int(x)

def printTariff():
    tariff = sys.argv[2]
    fdata = open(sys.argv[1])
    mtariff = tariffs[tariff]['minutes'] # 0.022 - 0.027
    dtariff = tariffs[tariff]['data']
    total = 0

    print "time  - cost"
    print "------------"
    for line in fdata.readlines():
        match = parser.match(line)
        (hours, mins, secs) = map(evaluator, match.groups())
        minutes = int(hours)*MINUTES + int(mins) + int(secs)/MINUTES
        cost = minutes*mtariff + ESTABLISHMENT    
        print "%s - %s" % (match.group(0), cost)
        total += cost
        
    print "------------"
    print "calls: %s €" % total
    total += dtariff
    print "calls + %s data plan : %s €" % (dtariff, total)
    vat = total*IVA
    total += vat
    print "VAT: %s €" % vat
    print "------------"    
    print "TOTAL: %s €" % total
    print "------------"

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print >> sys.stderr, "usage: %s file tariff" % sys.argv[0]
        exit(-1)
    printTariff()
