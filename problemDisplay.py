from drawText import draw_text
from fractionHandler import Fraction
import pygame
import colors
import pygame as pg

class ProblemDisplay:
    def __init__(self, screen, WIDTH, HEIGHT, stateManager,operationType):
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.stateManager = stateManager

        #drawing vars
        self.font = pygame.font.SysFont('Arial', 25)
        self.yDraw = self.HEIGHT-600 # medium y value for drawing problem/answer
        self.xOffset = 40 # x distance between each symbol or fraction
        self.xMid = int(self.WIDTH / 2)
        self.numeratorY = self.HEIGHT - 620
        self.denominatorY = self.HEIGHT -580
        self.fractionDividerY = self.HEIGHT - 600

        # get operation type to decide on symbol, ie "x" or "/" or "+"
        self.operation = ""
        if (operationType == 0): 
            self.operation = "Multiplication" 
            self.operationSymbol = 'x'
        elif (operationType == 1): 
            self.operation = "Addition" 
            self.operationSymbol = '+'
        elif (operationType == 2):
            self.operation = "Subtraction"
            self.operationSymbol = '-'
        elif (operationType == 3): 
            self.operation = "Division" 
            self.operationSymbol = '/'

        self.hasRightAnswer = False # Draw sprites depending on right answer

        # set problem fractions here -> change to dynamic set from RNG class later
        self.numerator1 = -1
        self.denominator1 = -1
        self.numerator2 = -1
        self.denominator2 = -1
        self.numeratorAnswer = -1
        self.denominatorAnswer = -1
        self.leadcoAnswer = -1

        self.usernumerator = -1
        self.userdenominator = -1

        #sprites
        self.checkmark = pg.image.load('assets/checkmark.png')
        self.x = pg.image.load('assets/x.png')

        self.yOffset = 0
        if self.operation == "Addition":
            self.yOffset = -50

    # called in draw function to easily draw each fraction
    def drawFraction(self,numerator,denominator,xPos):
        draw_text(str(numerator), self.font, (0,0,0), self.screen, xPos, self.numeratorY + self.yOffset)
        pygame.draw.line(self.screen,colors.BLACK, [xPos-10, self.fractionDividerY + self.yOffset], [xPos+10,self.fractionDividerY + self.yOffset], 3)
        draw_text(str(denominator), self.font, (0,0,0), self.screen, xPos, self.denominatorY + self.yOffset)

    def drawFractionMixed(self,leadco,numerator,denominator,xPos):
        if (numerator != 0):
            draw_text(str(leadco), self.font, (0,0,0), self.screen, xPos - 20, self.fractionDividerY + self.yOffset)
            draw_text(str(numerator), self.font, (0,0,0), self.screen, xPos, self.numeratorY + self.yOffset)
            pygame.draw.line(self.screen,colors.BLACK, [xPos-10, self.fractionDividerY + self.yOffset], [xPos+10,self.fractionDividerY + self.yOffset], 3)
            draw_text(str(denominator), self.font, (0,0,0), self.screen, xPos, self.denominatorY + self.yOffset)
        else:
            draw_text(str(leadco), self.font, (0,0,0), self.screen, xPos - 20, self.fractionDividerY + self.yOffset)

    # draw all fractions and symbols between fractions for current problem+answer
    def draw(self):
        if (self.stateManager.getCurrentState() != "Finished"): # only draw two problem fractions and x symbol
            draw_text(self.operationSymbol,self.font,(0,0,0),self.screen,self.xMid,self.yDraw+self.yOffset)
            self.drawFraction(self.numerator1,self.denominator1,self.xMid - self.xOffset)
            self.drawFraction(self.numerator2,self.denominator2,self.xMid + self.xOffset)
            if (self.stateManager.getCurrentState() == "Shading Horizontally"):
                self.userdenominator = self.stateManager.get_answerDenom()
        elif (self.stateManager.getCurrentState() == "Finished"):
            if self.stateManager.operation_type == 2 or self.stateManager.operation_type == 4: # division or addition
                self.userdenominator = self.stateManager.get_answerDenom()
            self.usernumerator = self.stateManager.get_answerNumer()
            userAnswer = Fraction(self.usernumerator, self.userdenominator)
            cpuAnswer = Fraction(self.numeratorAnswer, self.denominatorAnswer)
            canreduce = False
            cpucanreduce = False
            ismixed = False
            cpuismixed = False

            if userAnswer.isImproper() == True and cpuAnswer.isImproper() == True:
                ismixed = True
                cpuismixed = True
                userAnswer.makeMixed()
                cpuAnswer.makeMixed()
                self.leadcoAnswer = cpuAnswer.getLeadC()
                # userAnswer.denominator = cpuAnswer.denominator
            elif userAnswer.canReduce() == True:
                canreduce = True
                # cpucanreduce = True
            elif cpuAnswer.canReduce():
                cpucanreduce = True
            else:
                pass
                # userAnswer.denominator = cpuAnswer.denominator


            if canreduce == True: # user answer can be reduced so theres 7 total symbols
                userAnswerReduced = Fraction(userAnswer.getNum(),userAnswer.getDenom())
                userAnswerReduced.finalReduce()
                cpuAnswerReduced = Fraction(cpuAnswer.getNum(),cpuAnswer.getDenom())
                if cpuAnswerReduced.canReduce():
                    cpuAnswerReduced.finalReduce()
                # if user num and denom match known problem num and denom they got it right -> set isEqualSymbol to =
                if userAnswerReduced.getNum() == cpuAnswerReduced.getNum() and userAnswerReduced.getDenom() == cpuAnswerReduced.getDenom():
                    isEqualSymbol = '='
                    self.hasRightAnswer = True
                else:
                    isEqualSymbol = '=/='
                    self.hasRightAnswer = False
                draw_text(isEqualSymbol,self.font,(0,0,0),self.screen,self.xMid,self.yDraw + self.yOffset)
                #draw stuff from left of equal sign moving left
                self.drawFraction(self.numerator2,self.denominator2,self.xMid - self.xOffset)
                draw_text(self.operationSymbol,self.font,(0,0,0),self.screen,self.xMid- self.xOffset * 2,self.yDraw + self.yOffset)
                self.drawFraction(self.numerator1,self.denominator1,self.xMid - self.xOffset*3)
                #draw stuff from right of equal sign moving right
                self.drawFraction(userAnswer.getNum(),userAnswer.getDenom(),self.xMid + self.xOffset)
                draw_text('=', self.font, (0,0,0),self.screen,self.xMid + self.xOffset * 2,self.yDraw + self.yOffset)
                userAnswerReduced.finalReduce()
                self.drawFraction(userAnswerReduced.getNum(),userAnswerReduced.getDenom(),self.xMid + self.xOffset * 3)
                if self.hasRightAnswer: # draw checkmark
                    self.drawSprite(self.checkmark,True,0)
                else:
                    self.drawSprite(self.x,True,0) # draw x b/c user wrong
            elif ismixed == True or cpuismixed == True: # user answer is a mixed fraction so there will be 6 symbols
                tempUserAnswer = Fraction(self.usernumerator, self.userdenominator)
                tempCpuAnswer = Fraction(self.numeratorAnswer, self.denominatorAnswer)
                if tempUserAnswer.canReduce():
                    tempUserAnswer.finalReduce()
                if tempCpuAnswer.canReduce():
                    tempCpuAnswer.finalReduce()

                if userAnswer.getNum() == cpuAnswer.getNum() and userAnswer.getDenom() == cpuAnswer.getDenom() and userAnswer.getLeadC() == cpuAnswer.getLeadC() or (self.usernumerator / self.userdenominator == 1 and self.numeratorAnswer / self.denominatorAnswer == 1 or (tempCpuAnswer.numerator == tempUserAnswer.numerator and tempCpuAnswer.denominator == tempUserAnswer.denominator)):
                    isEqualSymbol = '='
                    self.hasRightAnswer = True
                else:
                    isEqualSymbol = '=/='
                    self.hasRightAnswer = False
                #left side
                self.drawFraction(self.numerator2,self.denominator2,self.xMid - self.xOffset)
                draw_text(self.operationSymbol,self.font,(0,0,0),self.screen,self.xMid- self.xOffset * 2,self.yDraw+ self.yOffset)
                self.drawFraction(self.numerator1,self.denominator1,self.xMid - self.xOffset*3)
                #right side
                draw_text(isEqualSymbol,self.font,(0,0,0),self.screen,self.xMid,self.yDraw+ self.yOffset)
                self.drawFractionMixed(userAnswer.getLeadC(),userAnswer.getNum(),userAnswer.getDenom(),self.xMid + self.xOffset)
                if self.hasRightAnswer: # draw checkmark
                   self.drawSprite(self.checkmark,False,-50)
                else:
                   self.drawSprite(self.x, False,-50) # draw x because user wrng
            else: #canreduce = False so there will be 5 symbols
                tempUserAnswer = Fraction(self.usernumerator, self.userdenominator)
                if tempUserAnswer.canReduce():
                    tempUserAnswer.finalReduce()
                if userAnswer.getNum() == self.numeratorAnswer and userAnswer.getDenom() == self.denominatorAnswer or (self.usernumerator == 0 and self.numeratorAnswer == 0 or (tempUserAnswer.numerator == self.numeratorAnswer and tempUserAnswer.denominator == self.denominatorAnswer)):
                    isEqualSymbol = '='
                    self.hasRightAnswer = True
                else:
                    isEqualSymbol = '=/='
                    self.hasRightAnswer = False
                self.drawFraction(self.numerator2,self.denominator2,self.xMid) # draw problem fraction 2 1st because itll be in middle
                draw_text(self.operationSymbol,self.font,(0,0,0),self.screen,self.xMid- self.xOffset,self.yDraw + self.yOffset)
                self.drawFraction(self.numerator1,self.denominator1,self.xMid - self.xOffset * 2)
                draw_text(isEqualSymbol,self.font,(0,0,0),self.screen,self.xMid + self.xOffset,self.yDraw + self.yOffset)
                self.drawFraction(userAnswer.getNum(),userAnswer.getDenom(),self.xMid + self.xOffset * 2)
                if self.hasRightAnswer: # draw checkmark
                    self.drawSprite(self.checkmark,False,0)
                else:
                    self.drawSprite(self.x, False,0) # draw x because user wrng

    def drawSprite(self,sprite,isReduced,xSymbolOffset): # isReduced param affects x offset of image drawn
        if isReduced == True:
            self.screen.blit(sprite,(self.xMid + self.xOffset * 4 - 10 + xSymbolOffset,self.yDraw - 30 + self.yOffset))
        else:
            self.screen.blit(sprite,(self.xMid + self.xOffset * 3 - 10 + xSymbolOffset,self.yDraw - 30 + self.yOffset))
    # this function called by problemGenerator class in getProblem method
    def setProblem(self,n1,d1,n2,d2,nAnswer,dAnswer):
        self.numerator1 = n1
        self.denominator1 = d1
        self.numerator2 = n2
        self.denominator2 = d2
        self.numeratorAnswer = nAnswer
        self.denominatorAnswer = dAnswer

                    
