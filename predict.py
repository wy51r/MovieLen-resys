#!/usr/bin/env python

import sys
from pprint import pprint
from database import *
from models.biasFromMean import *
from models.itemBased import *
from utils import *
from utils.metrics import *
def main(argv):
    db = Database('data/ml-data-100k')
    if 'stats' in argv:
        db.summary()

    if 'bias' in argv:
        print("The bias from mean methods:")
        bfm = BiasFromMean(db)
        bfm.model()
        observations = []
        forecasts = []
        for pair in db.test_pairwise:
            pre_rate = bfm.predict(pair[0],pair[1])
            observations.append(pair[2])
            forecasts.append(pre_rate)
        mae = MAE(observations, forecasts)
        rmse = RMSE(observations, forecasts)
        print("MAE = %.3f\tRMSE = %.3f" % (mae, rmse))
    if 'item-based' in argv:
        print("The item-based method:")
        item_based = ItemBased(db)
        item_based.model()
        observations = []
        forecasts = []
        for pair in db.test_pairwise:
            pre_rate = item_based.predict(pair[0], pair[1])
            forecasts.append(pre_rate)
            observations.append(pair[2])
            print("rate %.3f\t%d" % (pre_rate,pair[2]))
        mae = MAE(observations, forecasts)
        rmse = RMSE(observations, forecasts)
        print("MAE = %.3f\tRMSE = %.3f" % (mae, rmse))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
