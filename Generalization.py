texthandle = open("Aircraft - Allied.txt", 'r')
plane = input("Please enter the plane name: ")
terms = plane.split(" ")
print(terms)
possibilities = []
for n in range(len(terms)):    
    for line in texthandle:
        if line.lower().startswith(terms[0]):
            possibilities.append(line)
for thing in possibilities:
    print(thing)