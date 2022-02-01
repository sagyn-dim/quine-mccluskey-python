class Implicant:

    def __init__(self, minterm = 0, literal = 2):
        self.bin_repr = bin(minterm)[2:]        #Converting minterm to binary, FIRST INSTANCE ATTRIBUTE
        while len(self.bin_repr) < literal:     #Adding zeros so it corresponds to the number of literals
            self.bin_repr = '0' + self.bin_repr

        self.minterms = [self.bin_repr]         #Minterms in the given implicant, SECOND INSTANCE ATTRIBUTE

        self.group = 0                          #Grouping according to number of ones, THIRD INSTANCE ATTRIBUTE
        for i in self.bin_repr:
            if i == '1':
                self.group = self.group + 1

        self.matched = False                    #Initializing if matched boolean, FOURTH INSTANCE ATTRIBUTE

        self.pairs = []                         #Initializing list to store pairs, FIFTH INSTANCE ATTRIBUTE


    def pairToImplicant(implicant1, implicant2, literal):
        obj = Implicant()
        obj.bin_repr = ''
        for x in range(0,literal):
            if (implicant1.bin_repr[x] == implicant2.bin_repr[x]):
                obj.bin_repr = obj.bin_repr + implicant1.bin_repr[x]
            else: obj.bin_repr = obj.bin_repr + "_"

        obj.minterms = implicant1.minterms + implicant2.minterms

        obj.group = 0
        for i in obj.bin_repr:
            if i == '1':
                obj.group = obj.group + 1
        return obj



