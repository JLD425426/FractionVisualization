import random
from fractionHandler import Fraction
class ProblemGenerator:
    def __init__(self):
        self.problemDisplay = None
        self.operationType = None

        self.needsNewProblem = True
        self.currentProblem = None

    def setProblemDisplay(self,problemDisplay):
        self.problemDisplay = problemDisplay

    # get self.operationType which will be used to decide function for getProblem function
    def setOperationType(self,operationType):
        if operationType == 0: # multx
            self.operationType = "Multiplication"
        elif operationType == 1: # add
            self.operationType = "Addition"
        elif operationType == 2: # subtr
            self.operationType = "Subtraction"
        elif operationType == 3: #div
            self.operationType = "Division"

    # call correct getProblem function based off operation type
    def getProblem(self):
        if self.operationType == "Multiplication":
            self.getProblemMultiplication()
        elif self.operationType == "Addition":
            self.getProblemAddition()
        elif self.operationType == "Subtraction":
            self.getProblemSubtraction()
        elif self.operationType == "Division":
            self.getProblemDivision()

    def getProblemMultiplication(self):
        nAns = -1
        dAns = -1
        while True:
            n1 = random.randint(1,6)
            d1 = random.randint(1,6)
            n2 = random.randint(1,6)
            d2 = random.randint(1,6)
            nAns = n1 * n2
            dAns = d1 * d2
            if n1 >= d1: # on to next loop b/c mixed fraction, ie 3/2 
                continue
            if n2 >= d2: # same thing, mixed fraction
                continue
            if nAns < dAns:
                break
        # now reduce problem answer
        answer = Fraction(nAns,dAns)
        answer.isImproper()
        if answer.getMix() == True:
            answer.makeMixed()
        if answer.canReduce():
            answer.finalReduce()
        self.currentProblem = FractionProblem(n1,d1,n2,d2,answer.numerator,answer.denominator)
        self.problemDisplay.setProblem(n1,d1,n2,d2,answer.numerator,answer.denominator)

    def getProblemAddition(self):
        pass
    def getProblemSubtraction(self):
        pass
    def getProblemDivision(self):
        nAns = -1
        dAns = -1
        while True:
            n1 = random.randint(1,6)
            d1 = random.randint(1,6)
            n2 = random.randint(1,6)
            d2 = random.randint(1,6)
            nAns = n1 * d2
            dAns = d1 * n2
            if d1 == 1 or d2 == 1:
                continue
            if ((nAns) / (dAns)) >= 1: # answer too big, loop again
                continue
            if n1 > d1 or n2 > d2: # if num bigger than denom, loop again
                continue
            if n1 == d1 or n2 == d2: # loop again if fraction == 1
                continue
            else:
                break
        # now reduce problem answer
        answer = Fraction(nAns,dAns)
        answer.isImproper()
        if answer.getMix() == True:
            answer.makeMixed()
        if answer.canReduce():
            answer.finalReduce()
        self.currentProblem = FractionProblem(n1,d1,n2,d2,answer.numerator,answer.denominator)
        self.problemDisplay.setProblem(n1,d1,n2,d2,answer.numerator,answer.denominator)

    def resetCurrentProblem(self):
        n1 = self.currentProblem.num1
        d1 = self.currentProblem.den1
        n2 = self.currentProblem.num2
        d2 = self.currentProblem.den2
        nAns = self.currentProblem.numAnswer
        dAns = self.currentProblem.denAnswer
        self.problemDisplay.setProblem(n1,d1,n2,d2,nAns,dAns)


class FractionProblem:
    def __init__(self, num1, den1, num2,den2,numAnswer,denAnswer):
        self.num1 = num1
        self.den1 = den1
        self.num2 = num2
        self.den2 = den2
        self.numAnswer = numAnswer
        self.denAnswer = denAnswer

