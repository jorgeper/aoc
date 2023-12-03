# https://adventofcode.com/2023/day/3
# ugly c-like code in python!
file = open('machine.txt', 'r')
lines = file.readlines()

# turn strings into a matrix m representing the machine
m = []
for line in lines:
    m.append(list(line[:-1]))

# returns the part number if there's a part  in row j at position i
# it also wipes it out from the machine by replacing it with dots
# assumes part numbers don't start with 0
def getPart(m, i, j, parts):
    # check bounds
    if (j < 0 or j > len(m) or i < 0 or i > len(m[0])):
        return 0

    line = m[j]
    n = 0

    # read backwards from i (included)
    x = i
    mul = 1
    while (x >= 0):
        d = ord(line[x]) - 48
        if (d < 0 or d > 9):
            break
        n = d * mul + n
        mul = mul * 10
        line[x] = '.' # wipe it
        x -= 1
    
    if (n == 0):
        return 0

    # read forwards from i
    x = i + 1
    while (x < len(line)):
        d = ord(line[x]) - 48
        if (d < 0 or d > 9):
            break
        n = n * 10 + d
        line[x] = '.' # wipe it
        x += 1

    parts.append(n)
    return n

# returns sum of parts around a point (i, j) in a row of the machine
def getPartsInRow(m, i, j, parts):
    n = 0
    if (j < 0 or j >= len(m)):
        return 0
    n += getPart(m, i-1, j, parts)
    n += getPart(m, i,   j, parts)
    n += getPart(m, i+1, j, parts)
    return n

# returns sum of any parts around a point (i, j) in the machine
def getParts(m, i, j, parts):
    n = 0
    n += getPartsInRow(m, i, j, parts)
    
    # scan line above
    if (j > 0):
        n += getPartsInRow(m, i, j-1, parts)

    # scan line below
    if (j < len(m) - 1):
        n += getPartsInRow(m, i, j+1, parts)
        
    return n

# naive algorithm scans every row for symbols, reads parts around them, wipes them out as it goes
# parts stores all the found parts for debugging
# turns out it comes handy to use it for returning gear ratios for part 2 of the problem
# trivial to get rid of it for that purpose but I don't care
parts = []
dot = ord('.')
j = 0
n = 0
r = 0
while (j < len(m)):
    line = m[j]
    i = 0
    while (i < len(line)):
        d = ord(line[i])
        if d != dot and (d < 48 or d > 57): # not a dot nor a digit
            before = len(parts)
            n += getParts(m, i, j, parts)
            after = len(parts)

            # if it's a gear, calculate the gear ratio
            # this can be done without the parts array
            if (after - before == 2 and line[i] == '*'):
                r += parts[-1] * parts[-2]
        i += 1
    j += 1

# print (parts)
print ("parts: " + str(n))
print ("ratios: " + str(r))
