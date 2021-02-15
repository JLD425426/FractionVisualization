import pygame as pg
import random

#TODO:
#1) Figure out how to return or create new fractions
#1!) Return numerator and denominator in same line
#2) Figure out how to determine least common denominator
#2!) Have the two denominators be used to multiply into each other  
#3) Figure out way to tell IF least common denom can be found
#3!) Function for checking least common denominator
#4) Figure out way to display fractions nicely
#4?) Format found, display tbd
#5) Determine if/when we use this to check user's work
#5?) Might move to new class or alter this class to cover all problems


class Fraction:

    def __init__(self, numer, denom):
        self.numerator = numer
        self.denominator = denom
        self.isMixed = False
        self.leadCo = 0

    def getNum(self):
        return self.numerator

    def getDenom(self):
        return self.denominator

    def setNum(self, n):
        self.numerator = n

    def setDen(self, d):
        self.denominator = d

    def setMix(self, m):
        self.isMixed = m

    def getMix(self):
        return self.isMixed

    def getLeadC(self):
        return self.leadCo

    def isImproper(self):
        if (self.numerator >= self.denominator):
            self.isMixed = True
            return True
        else:
            self.isMixed = False
            return False

    def makeMixed(self):
        self.leadCo = (int)(self.numerator / self.denominator)
        self.numerator = (int)(self.numerator % self.denominator)
        #if self.numerator <= self.denominator:
        #    newNumer = (int)(self.numerator % self.denominator)
        #    self.numerator = newNumer
        
        

    def canReduce(self):
     #Determines whether a given fraction can be reduced or not
     #Returns true if it can reduce
     #Returns false if if cannot
        if self.numerator == 1:
            return False
        elif self.numerator == 0:
            return False
        elif self.denominator == 25 and self.numerator % 5 == 0:
            return True
        elif self.numerator != 0 and self.denominator % self.numerator == 0:
            return True
        elif self.numerator % 3 == 0 and self.denominator % 3 == 0:
            return True
        elif self.numerator % 2 == 0 and self.denominator % 2 == 0:
            return True
        else:
            return False

    def finalReduce(self):
     #Reduces the fraction given to the lowest form possible
     #Alters the original fraction
     #ASSUMES that the fraction can be reduced
        simplN = self.numerator
        simplD = self.denominator
        if simplD % simplN == 0:
            divide = int(simplD / simplN)
            simplN = 1
            simplD = divide
        else:
            if simplN % 3 == 0 and simplD % 3 == 0:
                simplN = int(self.numerator/3)
                simplD = int(self.denominator/3)
                while simplN % 3 == 0 and simplD % 3 == 0:
                    simplN = int(simplN/3)
                    simplD = int(simplD/3)
            if simplN % 2 == 0 and simplD % 2 == 0:
                simplN = int(self.numerator/2)
                simplD = int(self.denominator/2)
                while simplN % 2 == 0 and simplD % 2 == 0:
                    simplN = int(simplN/2)
                    simplD = int(simplD/2)
        self.numerator = simplN
        self.denominator = simplD


    def fAdd(self, numer2, denom2):
     #Computes the sum of two fractions and proportions accordingly if need be
     #Returns the new numerator and denominator
        if(self.denominator == denom2):
            sumNum = self.numerator + numer2
        else:
            temp = self.denominator
            self.numerator, self.denominator = self.fProportion(self.numerator, self.denominator, denom2)
            numer2, denom2 = self.fProportion(numer2, denom2, temp)
            sumNum = self.numerator + numer2
        return sumNum, self.denominator

    def fSub(self, numer2, denom2):
     #Computes the difference of two fractions and proportions accordingly if need be
     #Returns the new numerator and denominator
        if(self.denominator == denom2):
            difNum = self.numerator - numer2
        else:
            temp = self.denominator
            self.numerator, self.denominator = self.fProportion(self.numerator, self.denominator, denom2)
            numer2, denom2 = self.fProportion(numer2, denom2, temp)
            difNum = self.numerator - numer2
        return difNum, self.denominator
    
    def fMul(self, numer2, denom2):
        prodNum = self.numerator * numer2
        prodDen = self.denominator * denom2
        return prodNum, prodDen
    
    def fDiv(self, numer2, denom2):
        quoNum = self.numerator * denom2
        quoDen = self.denominator * numer2
        return quoNum, quoDen
    
    def fProportion(self, n, d, equiv):
     #Multipies the fraction and ensures equivalent size
        nNew = n * equiv
        dNew = d * equiv
        return nNew,dNew
