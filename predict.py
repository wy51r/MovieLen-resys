#!/usr/bin/env python

import sys
from pprint import pprint
from database import *

def main(argv):
    db = Database('data/ml-data-100k')
    if 'stats' in argv:
        db.summary()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
