# https://adventofcode.com/2023/day/2
# ugly c-like code in python!
# doesn't do any validation of input in the file format
file = open('input.txt', 'r')
lines = file.readlines()

R = 0
G = 1
B = 2
ID = 3
DONE = 4

MAX_R = 12
MAX_G = 13
MAX_B = 14

MAX_BALLS = 0xdeadbeef # some theoretical max number of balls

# returns a number starting at character i
# assumes no filler chars
def getNumber(line, i):
    n = 0
    d = ord(line[i])
    while (d >= 48 and d <= 57):
        n = n * 10 + (d - 48)
        i += 1
        d = ord(line[i])

    return n, i

# returns [TOKEN, i] where TOKEN is one of R, G, or B and i is the next position of the index
# assumes current char is one of 'r', 'g', or 'b'
def getRGB(line, i):
    c = line[i]
    if (c == 'r'):
        return R, i + 3 # skip "ed"
    elif (c == 'g'):
        return G, i + 5 # skip "reen"    
    else: # blue
        return B, i + 4 # skip "lue"

# returns new index skipping filler characters at the given index
def skipFillers(line, i):
    while (i < len(line) and (line[i] == ';' or line[i] == ' ' or line[i] == ':' or line[i] == ',' or line[i] == '\n')):
        i += 1
    return i

# returns [TOKEN, n, i] where n is:
# - the number of balls if TOKEN is RED, GREEN, or BLUE
# - the ID if TOKEN is ID
# - 0 if we reached the end of the line
def getNext(line, i):
    i = skipFillers(line, i)
    if (i >= len(line)):
        return DONE, 0, i

    # Game
    c = line[i]
    if (c == 'G'):
        n, i = getNumber(line, i + 5) # skip "Game "
        return ID, n, i
    
    # <number> <token>
    n, i = getNumber(line, i)
    if (i < len(line)):
        i = skipFillers(line, i)
        rgb, i = getRGB(line, i)
        return rgb, n, i
    else:
        return DONE, 0, i

# returns new [min, max] comparing n to given min and max
def getMinMax(n, min, max):
    return min if n > min else n, max if n < max else n

# return [possible?, max red, max green, max blue]
def processLine(line):
    minR, minG, minB = MAX_BALLS, MAX_BALLS, MAX_BALLS
    maxR, maxG, maxB = -MAX_BALLS, -MAX_BALLS, -MAX_BALLS

    i = 0
    t, n, i = getNext(line, i)
    while (t != DONE):
        if (t == ID):
            id = n
        elif (t == R):
            minR, maxR = getMinMax(n, minR, maxR)
        elif (t == G):
            minG, maxG = getMinMax(n, minG, maxG)
        elif (t == B):
            minB, maxB = getMinMax(n, minB, maxB)

        t, n, i = getNext(line, i)

    return id, maxR <= MAX_R and maxG <= MAX_G and maxB <= MAX_B, maxR, maxG, maxB

sumPossible = 0
sumPower = 0
for line in lines:
    id, possible, maxR, maxG, maxB = processLine(line)
    if (possible):
        sumPossible += id
    sumPower += (maxR * maxG * maxB)

print("possible:" + str(sumPossible))
print("power:" + str(sumPower))
