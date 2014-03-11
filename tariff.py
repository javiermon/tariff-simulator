#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- mode:python ; tab-width:4 -*- ex:set tabstop=4 shiftwidth=4 expandtab: -*-
# License: WTFPL
# http://sam.zoy.org/wtfpl/

from __future__ import division
import sys, re, os
from tariffs import tariffs
import logging
import optparse

IVA = 0.18
MINUTES = 60
PRECISION = "%.4f"
FORMAT = "%(asctime)s  [%(levelname)s]  [%(module)s] %(message)s"
BILLSDIR = 'bills/'

log = logging.getLogger('tariff')
parser = re.compile(r"(?:(\d{2}):)?(\d{2}):(\d{2})")
evaluator = lambda x: 0 if x is None else int(x)
floatsum = lambda x: float(PRECISION % sum(x))
nearpositive = lambda x: x if x >= 0 else 0
mthreshold = lambda x, y: x if not y else nearpositive(x - int(y))

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
        mtariff = [(tariffs[x]['minutes'], tariffs[x]['establishment'], tariffs[x]['threshold']) for x in tariff]
        # we need to apply the threshold tariff to the total minutes, we do it in mthreslhold.
        # [val1, val2, ..., valn]
        calls = [float(PRECISION % (mthreshold(minutes, threshold)*tariffm + establishment)) for (tariffm, establishment, threshold) in mtariff]

        log.debug( "%s - %s" % (match.group(0), calls))
        total = map(floatsum , zip(total, calls))

    log.debug("------------")
    log.debug("calls: %s €" % total)
    dtariff = [tariffs[x]['data'] for x in tariff]
    total = map(floatsum, zip(total, dtariff))
    log.debug("calls + %s data plan : %s €" % (dtariff, total))
    vat = map(lambda x: float(PRECISION % (x*IVA)), total)
    total = map(floatsum, zip(total, vat))

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
    # Setup the command line arguments.
    optp = optparse.OptionParser()

    # options.
    optp.add_option("-b", "--bill", dest="bill",
                    help="bill to process or 'all'.",)

    optp.add_option("-t", "--tariff", dest="tariff",
                    help="tariff for simulation from %s" % (tariffs.keys() + ['best']))

    optp.add_option("-v", "--verbose", dest="verbose",
                    help="log verbosity.", action="store_true")

    opts, args = optp.parse_args()

    if opts.bill is None:
        print >> sys.stderr, "no bill file provided"
        optp.print_help()
        sys.exit(1)

    if opts.tariff is None:
        print >> sys.stderr, "no tariff provided"
        optp.print_help()
        sys.exit(1)

    loglevel = logging.INFO if opts.verbose in (None, False) else logging.DEBUG

    # stderr logging:
    logging.basicConfig(format=FORMAT, level=loglevel)

    # find the best tariff?
    findbest = (opts.tariff == 'best')
    tariff = tariffs.keys() if findbest else [opts.tariff]
    # run all bills?
    if opts.bill == 'all':
        sumtotal = [0]*len(tariffs.keys())
        for filename in os.listdir(BILLSDIR):
            path = os.path.join(BILLSDIR, filename)
            if not os.path.isfile(path):
                continue
            fdata = open(path)
            (total, calls) = applyTariff(tariff, fdata)
            sumtotal = map(floatsum, zip(total,sumtotal))

        printTotal(sumtotal, tariff)
        if findbest:
            findBest(sumtotal)
    else:
        fdata = open(opts.bill)
        (total, calls) = applyTariff(tariff, fdata)
        if findbest:
            findBest(total)
