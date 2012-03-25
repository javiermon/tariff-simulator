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

def appyTariff(tariff, fdata):
    mtariff = tariffs[tariff]['minutes'] # 0.022 - 0.027
    dtariff = tariffs[tariff]['data']
    calls = 0
    total = 0

    log.debug("time  - cost")
    log.debug("------------")
    for line in fdata.readlines():
        match = parser.match(line)
        (hours, mins, secs) = map(evaluator, match.groups())
        minutes = int(hours)*MINUTES + int(mins) + int(secs)/MINUTES
        calls = minutes*mtariff + ESTABLISHMENT    
        log.debug( "%s - %s" % (match.group(0), calls))
        total += calls
        
    log.debug("------------")
    log.debug("calls: %s €" % total)
    total += dtariff
    log.debug("calls + %s data plan : %s €" % (dtariff, total))
    vat = total*IVA
    total += vat
    log.debug("VAT: %s €" % vat)
    log.debug("------------")   
    log.debug("TOTAL: %s €" % total)
    log.debug("------------")
    return (total, calls, dtariff)

if __name__ == '__main__':
    # stdout logging:
    logging.basicConfig(format=format, level=logging.DEBUG)

    if len(sys.argv) != 3:
        print >> sys.stderr, "usage: %s file tariff" % sys.argv[0]
        print >> sys.stderr, "where tariff in %s" % tariffs.keys()
        exit(-1)

    tariff = sys.argv[2]
    fdata = open(sys.argv[1])
    appyTariff(tariff, fdata)
