# -*- coding: utf-8 -*-
import pickle

with open("algs_dict.pkl", "rb") as f:
    a = pickle.load(f)
    print (a[501].solves_times)