#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- mode:python ; tab-width:4 -*- ex:set tabstop=4 shiftwidth=4 expandtab: -*-
# License: WTFPL
# http://sam.zoy.org/wtfpl/

from __future__ import division
import sys, re, os
from tariffs import tariffs
import logging

IVA = 0.18
MINUTES = 60
PRECISION = "%.4f"
FORMAT = "%(asctime)s  [%(levelname)s]  [%(module)s] %(message)s"
BILLSDIR = 'bills/'

log = logging.getLogger('tariff')
parser = re.compile(r"(?:(\d{2}):)?(\d{2}):(\d{2})")
evaluator = lambda x: 0 if x is None else int(x)

def applyTariff(tariff, fdata):
    total = [0]*len(tariffs.keys())
    
    log.info("------------")
    log.info("BILL FOR %s " % fdata.name)
    log.debug("time  - cost in %s" % tariff)
    log.debug("------------")
    for line in fdata.readlines():
        match = parser.match(line)
        (hours, mins, secs) = map(evaluator, match.groups())
        minutes = int(hours)*MINUTES + int(mins) + int(secs)/MINUTES
        mtariff = [(tariffs[x]['minutes'], tariffs[x]['establishment']) for x in tariff]
        calls = [float(PRECISION % (minutes*tariffm + tariffe)) for (tariffm, tariffe) in mtariff] # [val1, val2, ..., valn]
        
        log.debug( "%s - %s" % (match.group(0), calls))
        total = map(lambda x: float(PRECISION % sum(x)) , zip(total, calls))

    log.debug("------------")
    log.debug("calls: %s €" % total)
    dtariff = [tariffs[x]['data'] for x in tariff]
    total = map(lambda x: float(PRECISION % sum(x)), zip(total, dtariff))
    log.debug("calls + %s data plan : %s €" % (dtariff, total))
    vat = map(lambda x: float(PRECISION % (x*IVA)), total)
    total = map(lambda x: float(PRECISION % sum(x)), zip(total, vat))

    log.debug("VAT: %s €" % vat)
    log.debug("------------")   
    log.info("TOTAL: ")

    for (tar, amount) in zip(tariff, total):
        log.info("%s : %s €" % (tar, amount))
    log.info("------------")
    return (total, calls)

def findBest(total):
    best = min(total)
    winner = tariffs.keys()[total.index(best)]
    log.info("BEST TARIFF IS %s FOR %s €" % (winner, best))
    return (winner, best)

def printTotal(total, tariff):
    log.info("------------")
    log.info("GRAND TOTAL:")
    for (tar, amount) in zip(tariff, total):
        log.info("%s : %s €" % (tar, amount))
    log.info("------------")

if __name__ == '__main__':
    # stderr logging:
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    if len(sys.argv) != 3:
        print >> sys.stderr, "usage: %s file tariff" % sys.argv[0]
        print >> sys.stderr, "where tariff in %s" % tariffs.keys()
        exit(-1)

    tariff = sys.argv[2]
    # find the best tariff?
    findbest = (tariff == 'best')
    tariff = tariffs.keys() if findbest else [tariff]
    # run all bills?
    if sys.argv[1] == 'all':
        sumtotal = [0]*len(tariffs.keys())
        for filename in os.listdir(BILLSDIR):
            path = os.path.join(BILLSDIR, filename)
            if not os.path.isfile(path):
                continue
            fdata = open(path)
            (total, calls) = applyTariff(tariff, fdata)
            sumtotal = map(lambda x: float(PRECISION % sum(x)), zip(total,sumtotal))

        printTotal(sumtotal, tariff)
        if findbest:
            findBest(sumtotal)
    else:            
        fdata = open(sys.argv[1])
        (total, calls) = applyTariff(tariff, fdata)
        if findbest:
            findBest(total)

        
