import pygame as pg

#TODO:
#1) Figure out how to return or create new fractions
#2) Figure out how to determine least common denominator 
#3) Figure out way to tell IF least common denom can be found
#4) Figure out way to display fractions nicely
#5) Determine if/when we use this to check user's work


class Fraction:

    def __init__(self, numer, denom)
        self.numerator = numer
        self.denominator = denom

    def getNum(self)
        return self.numerator

    def getDenom(self)
        return self.denominator

    def setNum(self, n)
        self.numerator = n

    def setDen(self, d)
        self.denominator = d

    def fAdd(self, numer2, denom2)
        if(self.denominator == self.denominator)
            sumNum = self.numerator + numer2
        #else if found common denominator

    def fSub(self, numer2, denom2)
        if(self.denominator == denom2)
            difNum = self.numerator - numer2
        #else if found common denominator
    
    def fMul(self, numer2, denom2)
        prodNum = self.numerator * numer2
        prodDen = self.denominator * denom2
    
    def fDiv(self, numer2, denom2)
        quoNum = self.numerator * denom2
        quoDen = self.denominator + numer2
    
    def fComDenom(self, numer2, denom2)
        #this will be a doozy
    
    def fProportion(self, equiv)
        self.numerator = self.numerator * equiv
        self.denominator = self.denominator * equiv
