import difflib
from difflib import SequenceMatcher
import itertools

def search(plane):
    alliedaircraft = []             #all allied aircraft that could be considered useful
    texthandle = open("Aircraft - Allied.txt", 'r')         #open file that contains all useful allied aircraft
    for line in texthandle:                                 #iterate through text file
        alliedaircraft.append(line.strip())                 #add the aircraft names to the list
    axisaircraft = []
    texthandle2 = open("Aircraft - Axis.txt", 'r')
    for line in texthandle2:
        axisaircraft.append(line.lower())
    def cleanup2(plane):                                    #function for cleaning up whitespace and non-alpha-numeric characters
        plane = plane.replace("-", "")
        plane = plane.replace(" ", "")
        plane = plane.lower()
        plane = plane.replace("\n", "")
        plane = plane.replace("(", "")
        plane = plane.replace(")", "")
        return plane
    similarities = {}                                       #dictionary for holding all the planes and their respective match percentages
    plane = cleanup2(plane)
    for plane1 in alliedaircraft:                           #iterate through all allied planes
        if plane == cleanup2(plane1):                                 #if they are a perfect match
            similarities[plane1] = 100                      #set similarity percentage to 100 and break the while loop
            break
        elif len(plane) <= len(cleanup2(plane)):                     #if not a perfect match
            similarity = difflib.SequenceMatcher(None, plane, cleanup2(plane1)[:len(plane)+1]).ratio()    #calculate percent match
            similarities[plane1] = similarity * 100                                             #multiply by 100 for actual percent readings
    for plane1 in axisaircraft:                           #iterate through all allied planes
        if plane == cleanup2(plane1):                                 #if they are a perfect match
            similarities[plane1] = 100                      #set similarity percentage to 100 and break the while loop
            break
        elif len(plane) <= len(cleanup2(plane)):                     #if not a perfect match
            similarity = difflib.SequenceMatcher(None, plane, cleanup2(plane1)[:len(plane)+1]).ratio()    #calculate percent match
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
        if sortedlist[n][1] == samesims[0][1]:  #if the current similarity is equal to the previous one
            samesims.append(sortedlist[n])          #add that plane and its similarity
    print(samesims)
    shortestindex = 0                               #algorithm to determine what the plane with the shortest name is
    shortest = len(samesims[0][0])                  #set the shortest string length to be the first plane's string length
    for n in range(1, len(samesims)):               #iterate through the next terms of the list of planes with the same similarities
        if len(samesims[n][0]) < shortest:          #if the present plane has a shorter string length
            shortest = len(samesims[n][0])          #make the shortest length to be that length
            shortestindex = n                       #set the index of the shortest string length to be that index
    '''if samesims[shortestindex][1] > 50:                       #if the match found is reasonably comparable to the request'''
    print(samesims[shortestindex][0].replace("\n", "") + ", " + str(samesims[shortestindex][1]))   #return the plane with the highest match
    '''else:
        return "No match"'''

while True:
    plane = input("Please enter a request: ")
    search(plane)