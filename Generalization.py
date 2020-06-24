import difflib
from difflib import SequenceMatcher
import numpy as np
import itertools
alliedaircraft = []
texthandle = open("Aircraft - Allied.txt", 'r')
for line in texthandle:
    alliedaircraft.append(line.lower())
while True:
    similarities = {}
    plane = input("Please enter the plane name: ")
    plane = plane.replace("-", "")
    plane = plane.replace(" ", "")
    plane = plane.lower()
    for plane1 in alliedaircraft:
        plane1 = plane1.replace("-", "")
        plane1 = plane1.replace(" ", "")
        plane1 = plane1.replace("\n", "")
        if len(plane1) >= len(plane):
            similarity = difflib.SequenceMatcher(None, plane, plane1[:len(plane)]).ratio()
            similarities[plane1] = similarity * 100

    sortedlist = list()                 #creating empty list to hold sorted users
    for thing in similarities.items():     #iterate through the keys and terms of usercount dictionary
        sortedlist.append(thing)        #add each key,value pair to sortedlist
    for i in range(1, len(sortedlist)):         #insertion sort algorithm
        nextElementValue = sortedlist[i][1]
        temp = sortedlist[i]
        j = i-1
        while j >= 0 and sortedlist[j][1] < nextElementValue:
            item = sortedlist[j]
            sortedlist[j+1] = item
            j = j-1
        sortedlist[j+1] = temp
    print(sortedlist[0])