#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 10:03:58 2018

@author: Claire
"""
import pandas as pd
import random
import numpy as np

def pop_random(lst):
    idx = random.randrange(0, len(lst))
    return lst.pop(idx)

def runMatch(csvfile):
    NamesDB = pd.read_csv(csvfile)
    NamesPID = list(NamesDB.PID.values)
    pairs = []
    while len(NamesPID) > 0:
        rand1 = pop_random(NamesPID)
        rand2 = pop_random(NamesPID)
        pair = rand1, rand2
        pairs.append(pair)

    pairsnp = np.array(pairs)
    pairsDF = pd.DataFrame(pairsnp, columns = ('PersonA', 'PersonB'))
    return(pairsDF)