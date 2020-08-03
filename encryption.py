'''import random
import string
with open("SuperSecurePepegaEncryption.txt", "a+") as texthandle:
    randomnumber = random.randint(0, 1000000)
    print(randomnumber)
    for n in range(randomnumber):
        allletters = string.ascii_letters
        texthandle.write(random.choice(allletters))
    texthandle.write("2anjpsryvwofq6l21o5bhkywltsidw")
    randomnumber2 = random.randint(0, 1000000)
    print(randomnumber2)
    for n in range(randomnumber2):
        allletters = string.ascii_letters
        texthandle.write(random.choice(allletters))
texthandle.close()
'''
with open("SuperSecurePepegaEncryption.txt", "r") as texthandle:
    buildstring = ""
    for thing in texthandle:
        buildstring += thing
    print(buildstring.find("2anjpsryvwofq6l21o5bhkywltsidw"))
    print(buildstring[178655:178685])