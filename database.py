#!/usr/bin/env python

try:
    import cPickle as pickle
except:
    import pickle

from datetime import date
from collections import defaultdict
from math import log
from pprint import pprint
from utils import msg
import os
import time

class Database:
    def __init__(self,datadir):
        """Constroctor
        """
        self.datadir = datadir
        self.test_pairwise = []
        self.user_num = 0
        self.item_num = 0
        self.rating_num = 0

        self.fields = ['test_pairwise','user_num','item_num','rating_num']
    
        if self.pickle_jar():
            return

        fields = (
            #dict		key	=value
	    ("rating_item	item	=user, rating, date", list),
	    ("u_rating		user	=item, rating, date", list),
	    ("item_info		item	=title, date, date2, url, genre", list),
	    ("user_info		user	=age, gender, occupation, zipcode", list),
	    ("ocp_by_user	ocp	=user", list),
	    ("genre_by_item	genre	=item", list),
        )
        for defn, datatype in fields:
            name, key, _ = defn.split(None,2)
            setattr(self, name, defaultdict(datatype))
            self.fields.append(name)
        self.fields.sort()

        # collect data
        self.parse_rating()
        self.parse_info()
        self.parse_item()
        self.parse_user()
        
        self.fill_pickle()

    def pickle_jar(self):
        """Check whether we have load the dataset to pickle
        """
        jar = '/'.join((self.datadir,"pickle.jar"))
        if os.path.exists(jar):
            try:
                jarf = open(jar,'r')
                d = pickle.load(jarf)
                jarf.close()
            except:
                return False
            
            self.fields = d['fields']
            for field in self.fields:
                setattr(self,field,d[field])
            return True
        else:
            return False

    def fill_pickle(self):
        """Load the dataset to pickle
        """
        jar = '/'.join((self.datadir,"pickle.jar"))
        d = {}
        
        msg("Filling pickle jar '%s'" % jar)
        
        for field in self.fields:
            d[field] = getattr(self,field)
        d['fields'] = self.fields
        
        jarf = open(jar,'w')
        pickle.dump(d,jarf)
        jarf.close()

    def parse_rating(self):
        """Parse the rating data from 'u.data'

        Each user has rated at least 20 movie. Users and items are numbered
        consecutively from 1. The data is randomly ordered. This is a tab
        separated list of
          user id | item id | rating | timestamp.
        The time stamps are unix seconds since 1/1/1970 UTC

        """
        msg("parsing u.data")
        lines = file('/'.join((self.datadir,"u.data"))).read().split("\n")
        records = [[int(x) for x in line.split("\t")]
                   for line in lines if line]

        for user, item, rating, timestamp in records:
            self.rating_item[item].append((user,rating,timestamp))
            self.u_rating[user].append((item,rating,timestamp))

    def parse_info(self):
        """Parse the total user info from 'u.info'
        The number of users, items, and ratings in the u data set
        """
        msg("parsing u.info")
        lines = file('/'.join((self.datadir,"u.info"))).read().split("\n")
        # users
        pair = lines[0].split()
        self.user_num = int(pair[0])
        
        # items
        pair = lines[1].split()
        self.item_num = int(pair[0])

        # ratings
        pair = lines[2].split()
        self.rating_num = int(pair[0])
    
    def parse_item(self):
        """Parse the item info from 'u.item'
        Information about the items (movies); this is a tab separated
              list of
              movie id | movie title (release date) | video release date |
              IMDb URL | unknown | Action | Adventure | Animation |
              Children's | Comedy | Crime | Documentary | Drama | Fantasy |
              Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi |
              Thriller | War | Western |
              The last 19 fields are the genres, a 1 indicates the movie
              is of that genre, a 0 indicates it is not; movies can be in
              several genres at once.
              The movie ids are the ones used in the u.data data set.
        """
        msg("parsing u.item")
        lines = file('/'.join((self.datadir,"u.item"))).read().split("\n")
        infos = [line.replace('||','|').split('|') for line in lines if line]
        for info in infos:
            movie_id = int(info[0])
            if len(info[1].rstrip(')').rsplit(' (',1))==2:
                title, date1 = info[1].rstrip(')').rsplit(' (',1)
            else:
                title=info[1]
                date1 = ''
            release = 0
            if info[2]:
                release = time.strptime(info[2],"%d-%b-%Y")
            genres=info[-19:]
            self.item_info[movie_id]=(title,date1,release,info[3],genres)
            for i in xrange(len(genres)):
                if int(genres[i]) == 1:
                    self.genre_by_item[i].append(movie_id)
        

    def parse_genre(self):
        """Parse a list of movie genres from 'u.genre'
        """
        msg("parsing u.genre")
        lines = file('/'.join((self.datadir,"u.genre"))).read().split('\n')
        pairs = [line.split('|') for line in lines if line]


    def parse_user(self):
        """Parse user info from 'u.user'
        this is a tab
              separated list of
              user id | age | gender | occupation | zip code
              The user ids are the ones used in the u.data data set.
        """
        msg("parsing u.user")
        lines = file('/'.join((self.datadir,"u.user"))).read().split('\n')
        records = [line.split('|') for line in lines if line]
        pairs = [tuple([int(line[0]),
                        int(line[1]),
                        line[2],
                        line[3],
                        line[4]])
                 for line in records]
        for id, age, gender, occupation, zipcode in pairs:
            self.user_info[id]=(age, gender, occupation, zipcode)
            self.ocp_by_user[occupation].append(id)
    def parse_occupation(self):
        """Parse a list of the ccupations from 'u.occupation'
        """
        pass
    
    def parse_test(self):
        """Parse test user set from 'u*.test'
        """
        pass

    def summary(self, unabridged=False):
        """Summary info about the dataset
        """
        props = ("rating_item "
                 "u_rating "
                 "item_info "
                 "user_info "
                 "ocp_by_user "
                 "genre_by_item ").split()
        for prop in props:
            print(">> %s" % prop)
            if unabridged:
                pprint(dict(getattr(self, prop).items))
            else:
                pprint(dict(getattr(self, prop).items()[:3]))
            print("")
    
        msg("Test user item pairwise")
        if unabridged:
            pprint(self.test_pairwise)
        else:
            pprint(self.test_pairwise[:3])
