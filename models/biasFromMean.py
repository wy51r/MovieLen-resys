#!/usr/bin/env python

"""A Baseline Schemes, BIAS FROM MEAN
Notatin:
S(i): the set of user who have rated item 'i'
r(u,i): the rate of item 'i' rated by user 'u'
mean(u): the average rate of user 'u'

Predict Formulation:
p(u,i) = mean(u)+(1/len(S(i)))
                   *sum(r(v,i)-mean(v)) that user 'v' have rated item 'i'

Refference:
1. Lemire D, Maclachlan A. Slop one predictors for online rating-based collaborative filtering. 2005

"""

from collections import defaultdict
from pprint import pprint

class BiasFromMean:
    def __init__(self, data):
        """Constructor
        """
        self.data = data
        self.u_mean = {}
        
    
    def model(self):
        """ build the model
        """
        for user, ratings in self.data.u_rating.items():
            self.u_mean[user] = sum([rate[1] for rate in ratings])
            self.u_mean[user] /= len(ratings)
            
    
    def predict(self, user, item):
        """ predict user's rating
        """
        card = len(self.data.rating_item[item])
        bias = sum([(rating[1]-self.u_mean[rating[0]])
                    for rating in self.data.rating_item[item]])
        pre_rate = self.u_mean[user] + (1/card)*bias
        return pre_rate
    
    def recommend(self, user):
        """ generate recommendation for user
        """
        pass
        
