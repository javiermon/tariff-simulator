#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- mode:python ; tab-width:4 -*- ex:set tabstop=4 shiftwidth=4 expandtab: -*-
# License: WTFPL
# http://sam.zoy.org/wtfpl/

from __future__ import division
import sys, re
from tariffs import tariffs
import logging

IVA = 0.18
MINUTES = 60
ESTABLISHMENT = 0.15
format = "%(asctime)s  [%(levelname)s]  [%(module)s] %(message)s"

log = logging.getLogger('tariff')
parser = re.compile(r"(?:(\d{2}):)?(\d{2}):(\d{2})")
evaluator = lambda x: 0 if x is None else int(x)

def applyTariff(tariff, fdata):
    findbest = (tariff == 'best')
    tariff = tariffs.keys() if findbest else [tariff]
    total = [0]*len(tariffs.keys())

    log.debug("time  - cost")
    log.debug("------------")
    for line in fdata.readlines():
        match = parser.match(line)
        (hours, mins, secs) = map(evaluator, match.groups())
        minutes = int(hours)*MINUTES + int(mins) + int(secs)/MINUTES
                
        mtariff = map(lambda x: tariffs[x]['minutes'], tariff)
        calls = map(lambda x: float("%.4f" % (minutes*x + ESTABLISHMENT)), mtariff) # [val1, val2, ..., valn]
        
        log.debug( "%s - %s" % (match.group(0), calls))
        total = map(sum, zip(total, calls))
        

    log.debug("------------")
    log.debug("calls: %s €" % total)
    dtariff = [tariffs[x]['data'] for x in tariff]
    total = map(sum, zip(total, dtariff))
    log.debug("calls + %s data plan : %s €" % (dtariff, total))
    vat = map(lambda x: x*IVA, total)
    total = map(sum, zip(total, vat))

    log.debug("VAT: %s €" % vat)
    log.debug("------------")   
    log.debug("TOTAL: %s €" % total)
    log.debug("------------")
    if findbest:
        best = min(total)
        winner = tariffs.keys()[total.index(best)]
        log.debug("BEST TARIFF IS %s FOR %s €" % (winner,best))
        return (winner, best)
    return (total, calls)

if __name__ == '__main__':
    # stderr logging:
    logging.basicConfig(format=format, level=logging.DEBUG)

    if len(sys.argv) != 3:
        print >> sys.stderr, "usage: %s file tariff" % sys.argv[0]
        print >> sys.stderr, "where tariff in %s" % tariffs.keys()
        exit(-1)

    tariff = sys.argv[2]
    fdata = open(sys.argv[1])
    applyTariff(tariff, fdata)
