from implicant import Implicant
import sys

inputs = []
n = 0
#Zeroth step is to open the file and read the contents
f = open("input.txt", "r")
if f.mode == "r":
    f1 = f.readlines()
    mintermStr = f1[0].replace(" ", "").split(",")
    for i in mintermStr:
        try:
            inputs = inputs + [int(i)]
        except:
            print("Invalid input, minterm must given as integer seperated by commas")
            sys.exit()

    try:
        n = int(f1[1].strip())
    except:
        print("Invalid number of literals, must be given as an integer")

#First tep is to check the validity of the minterms
for i in inputs:
    if i < 0:
        print("Minterm must be greater than zero: " + str(i))
        sys.exit()
    if i > 2**n - 1:
        print("At least one invalid minterm for the given number of literals: " + str(i))
        sys.exit()
if n <= 0:
    print("Number of literals must be greater than zero")
    sys.exit()
#Second step is to create implicant objects for this minterms
implicants = []
for i in inputs:
    implicant_obj = Implicant(i, n)
    implicants = implicants + [implicant_obj]

#Repeat third and fourth step until there are no pairs
while True:
    for i in implicants:    #Third step is to find pairs which differ in one bit
        for k in implicants:
            if k.group == i.group + 1:
                numOfChanges = 0
                for x in range (0, n) :
                    if k.bin_repr[x] != i.bin_repr[x]:
                        numOfChanges += 1
                if numOfChanges == 1:
                    i.pairs = i.pairs + [k]
                    i.matched = True
                    k.matched = True

    noPairs = True
    for i in implicants:
        if i.matched:
            noPairs = False
            break

    #Fourth step is to merge paired implicants and create new list
    if not noPairs:
        newImplicants = []
        for i in implicants:
            if i.pairs:
                for k in i.pairs:
                    newImplicants = newImplicants + [Implicant.pairToImplicant(i, k, n)]
            elif not i.matched:
                newImplicants = newImplicants + [i]
        implicants = newImplicants
    else: break

#Fifth step is to eliminate duplicates
primeImplicants = [implicants[0]]
for i in implicants:
    match = False
    for k in primeImplicants:
        if i.bin_repr == k.bin_repr:
            match = True
            break
    if not match:
        primeImplicants = primeImplicants + [i]

#Sixth step is to find essential prime implicants
essentialImplicants = []
nonEssential = []
for i in primeImplicants:
    isEssential = False
    for k in i.minterms:
        commonMinterm = False
        for l in primeImplicants:
            if i == l:
                continue
            else:
                for z in l.minterms:
                    if k == z:
                        commonMinterm = True
                        break
            if commonMinterm:
                break
        if not commonMinterm:
            isEssential = True
            break
    if isEssential:
        essentialImplicants = essentialImplicants + [i]
    else:
        nonEssential = nonEssential + [i]

#The seventh step is to find minimal number of prime implicants to cover the answer
for i in essentialImplicants:
    for k in i.minterms:
        for z in nonEssential:
            try:
                z.minterms.remove(k)
            except:
                continue
finalPrimeImplicants = []
while True:
    # for i in nonEssential:
    #     print(i.bin_repr + " ")
    #     print(i.minterms)
    #     print(" ")
    # print("-------------")
    toBreak = True
    for i in nonEssential:
        if i.minterms:
           toBreak = False
    if toBreak:
        break
    maxLen = 0
    numOfLiteral = n
    for i in nonEssential:
        if len(i.minterms) > maxLen:
            maxLen = len(i.minterms)
            maxPos = nonEssential.index(i)
            numOfLiteral = n - i.bin_repr.count('_')
        elif len(i.minterms) == maxLen:
            if n - i.bin_repr.count('_') < numOfLiteral:
                maxPos = nonEssential.index(i)
                numOfLiteral = n - i.bin_repr.count('_')

    finalPrimeImplicants = finalPrimeImplicants + [nonEssential[maxPos]]

    nonEssential.remove(nonEssential[maxPos])

    for k in finalPrimeImplicants[len(finalPrimeImplicants)-1].minterms:
        for z in nonEssential:
            try:
                z.minterms.remove(k)
            except:
                continue

#The eighth step is to display the implicants and write them in a txt file
str = "VWXYZ"
def letterRepr(binRepr):
    letters = ''
    if binRepr.find('1') == -1 and binRepr.find('0') == -1:
        letters = letters + "1"
    else:
        for k in range(0, n):
            if binRepr[k] == '0':
                letters = letters + str[k] + "'"
            elif binRepr[k] == '1':
                letters = letters + str[k]
    return letters

g = open("output.txt", "w+")
g.write("Here are all the prime implicants: \n")
for i in primeImplicants:
    g.write("[" + letterRepr(i.bin_repr) + "] ")

g.write("\n\nHere are all the essential implicants: \n")
for i in essentialImplicants:
    g.write("[" + letterRepr(i.bin_repr) + "] ")

g.write("\n\nHere is the optimized output:\n")
for i in essentialImplicants:
    g.write("[" + letterRepr(i.bin_repr) + "] ")
for i in finalPrimeImplicants:
    g.write("[" + letterRepr(i.bin_repr) + "] ")
g.close()

