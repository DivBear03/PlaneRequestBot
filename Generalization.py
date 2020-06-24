texthandle = open("Aircraft - Allied.txt", 'r')
plane = input("Please enter the plane name: ")
terms = plane.split(" ")
for line in texthandle:
    if plane == line: 
        print("Plane found: " + line)
    else:
        print("Plane not found")