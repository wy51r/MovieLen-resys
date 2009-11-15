#!/usr/bin/env python

import sys
from pprint import pprint
from database import *
from models.biasFromMean import *

def main(argv):
    db = Database('data/ml-data-100k')
    if 'stats' in argv:
        db.summary()
    bfm = BiasFromMean(db)
    bfm.model()
    for pair in db.test_pairwise:
        pre_rate = bfm.predict(pair[0],pair[1])
        print(">>>> %d %f %.3f" % (pair[2],pre_rate,(pre_rate-pair[2])))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
