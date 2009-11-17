#!/usr/bin/env python
from math import sqrt
from utils import *
from pprint import pprint
import sys

class ItemBased:
    def __init__(self,data):
        """Constructor
        """
        self.data = data
        self.u_mean = {}
        self.matrix = []
    
    def model(self):
        """building model
        """
        for user, ratings in self.data.u_rating.items():
            self.u_mean[user] = sum([rate[1] for rate in ratings])+0.0
            self.u_mean[user] /= len(ratings)
                

    def cosine_sim(self, item1, item2):
        """Cosine similarity between items
        """
        user1 = set(map(lambda x:x[0],self.data.rating_item[item1]))
        user2 = set(map(lambda x:x[0],self.data.rating_item[item2]))
        commons = user1 & user2

        e_ij = []
        e_i = []
        e_j = []
        for user in commons:
            u_ij = filter(lambda x:(x[0]==item1 or x[0]==item2),
                        self.data.u_rating[user])
            e_ij.append((u_ij[0][1]-self.u_mean[user])*\
                            (u_ij[1][1]-self.u_mean[user]))
            e_i.append((u_ij[0][1]-self.u_mean[user])**2)
            e_j.append((u_ij[1][1]-self.u_mean[user])**2)
        try:
            sim = sum(e_ij)/(sqrt(sum(e_i))*sqrt(sum(e_j)))
        except ZeroDivisionError:
            #msg("The second number can't be zero!")
            sim = 1 # cos(0) = 1
        return sim

    def recommend(self,user):
        """Recommendation for user
        """
        pass
    
    def predict(self, user, item):
        """Predict user's rate for item
        """

        sims = map(lambda x: abs(self.cosine_sim(item,x[0])),
                      self.data.u_rating[user])

        sums = map(lambda x : x[1]*abs(self.cosine_sim(item,x[0])),
                      self.data.u_rating[user])
        try:
            prediction = sum(sums)/(sum(sims))
        except ZeroDivisionError:
            msg("The second number can't be zero!")

        return prediction


        
