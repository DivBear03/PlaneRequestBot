# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 12:45:43 2020

@author: Kailash
"""
import socket           #importing useful modules
import re
import time
import os 
import datetime
from datetime import timedelta
import difflib
from difflib import SequenceMatcher
import scipy.stats

#task: add algorithm which starts with gestalt but adds weight on order of matching characters
#task: add algorithm which separts alpha and numeric components of string and scores each individually, then recombines scores into one
#task: within numeric component, look for roman numerals

aircraft = []             #all allied aircraft that could be considered useful
texthandle = open("Aircraft.txt", 'r')         #open file that contains all useful allied aircraft
for line in texthandle:                                 #iterate through text file
    aircraft.append(line.strip())                 #add the aircraft names to the list
bombers = []
bombhandle = open("Bomber_Blacklist.txt", 'r')
for line in bombhandle:
    bombers.append(line.strip())
def time_convert(time_diff):                                                  #function for converting seconds into a readable time
    execution_time = time_diff.total_seconds()
    return execution_time

def cleanup2(plane):                                    #function for cleaning up whitespace and non-alpha-numeric characters
    plane = plane.replace("-", "")
    plane = plane.replace(" ", "")
    plane = plane.lower()
    plane = plane.replace("\n", "")
    plane = plane.replace("(", "")
    plane = plane.replace(")", "")
    return plane

def gestalt(plane,plane1):
    return (100 * difflib.SequenceMatcher(None, plane, cleanup2(plane1)[:len(plane)+1]).ratio())

def defSim(plane, plane1):
    return gestalt(plane, plane1)

def inSim(plane,plane1):
    if plane in cleanup2(plane1):
        return 100
    else:
        return defSim(plane,plane1)

def isSim(plane, plane1):
    if plane == cleanup2(plane1):
        return 110
    else:
        return defSim(plane,plane1)

def orderSim():
    pass
    
def compSim():
    pass
    
def mineditDist(plane,plane1):
    plane1 = cleanup2(plane1)
    len1 = len(plane) +1
    len2 = len(plane1) +1    
    matrix = [[0 for x in range(len1+1)] for y in range(len2+1)]
        
    for x in range(len2+1):
        matrix[x][0] = x
    for y in range(len1+1):
        matrix[0][y] = y

    for xx in range(1,len2):
        for yy in range(1,len1):
                
            if plane1[xx-1] == plane[yy-1]:
                matrix[xx][yy] = matrix[xx-1][yy-1]
            else:
                matrix[xx][yy] = min([matrix[xx-1][yy],matrix[xx][yy-1],matrix[xx-1][yy-1]]) + 1
                #print(xx,yy,matrix[xx][yy])   
    dist = matrix[len2-1][len1-1]
        
    ret = scipy.stats.norm(0,3).pdf(dist)/scipy.stats.norm(0,3).pdf(0)

    return ret*100

def search2(plane):
    
    plane = cleanup2(plane)

    if len(plane) <= 2:
        return "No match"

    for plane1 in bombers:
        substring = cleanup2(plane1)[:len(plane)]
        if plane in substring:
            return "Bombers are useless"
  
    similarities = {}                                       #dictionary for holding all the planes and their respective match percentages
    plane = cleanup2(plane)

    foreign = False
    if "usa" in plane or "ussr" in plane or 'japan' in plane or 'germany' in plane or 'italy' in plane or 'china' in plane or 'france' in plane or 'greatbritain' in plane:
        foreign = True


    if foreign == False:
        
        for plane1 in aircraft:
                
            sim1 = isSim(plane,plane1)       
            sim = defSim(plane, plane1)
            if sim < 60:
                similarities[plane1] = sim
                continue
            sim2 = inSim(plane,plane1)
            sim3 = mineditDist(plane, plane1)
            plane1 = plane1.replace("\n", "")            
            similarities[plane1] = (sim + sim1 + sim2 + .5*sim3)/4                                             
        
    else:
        for plane1 in aircraft:
            if plane == cleanup2(plane1):
                similarities[plane1] = 100
                break
            elif "[" in plane1 and len(plane) <= len(cleanup2(plane1)):
                similarity = gestalt(plane, plane1)
                plane1 = plane1.replace("\n", "")
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


    samesims = []                                   #list to hold all top results with the same similarity
    samesims.append(sortedlist[0])                  #add the top one
    for n in range(1, len(sortedlist)):
        if sortedlist[n][1] == samesims[0][1]:  #if the current similarity is equal to the similarity of the top result one
            samesims.append(sortedlist[n])          #add that plane and its similarity
    shortestindex = 0                               #algorithm to determine what the plane with the shortest name is
    shortest = len(samesims[0][0])                  #set the shortest string length to be the first plane's string length
    for n in range(1, len(samesims)):               #iterate through the next terms of the list of planes with the same similarities
        if len(samesims[n][0]) < shortest:          #if the present plane has a shorter string length
            shortest = len(samesims[n][0])          #make the shortest length to be that length
            shortestindex = n                       #set the index of the shortest string length to be that index
    if samesims[shortestindex][1] > 60:             #if the match found is reasonably comparable to the request
        return samesims[shortestindex]              #return the plane with the highest match
    else:
        return "No match"


while True:
    a = input("Search for:")
    if "end" in a:
        break
    startrequesttime = datetime.datetime.now()
    print(search2(a))
    print(time_convert(datetime.datetime.now()-startrequesttime))