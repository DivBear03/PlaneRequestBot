import difflib
from difflib import SequenceMatcher
import numpy as np
import itertools

texthandle = open("Aircraft - Allied.txt", 'r')
plane = input("Please enter the plane name: ")
alliedaircraft = []
similarities = {}
for line in texthandle:
    alliedaircraft.append(line.lower())
for plane1 in alliedaircraft:
    similarity = difflib.SequenceMatcher(None, plane, plane1).ratio()
    similarities[plane1] = similarity * 100

