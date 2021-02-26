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

    # called in draw function to easily draw each fraction
    def drawFraction(self,numerator,denominator,xPos):
        draw_text(str(numerator), self.font, (0,0,0), self.screen, xPos, self.numeratorY)
        pygame.draw.line(self.screen,colors.BLACK, [xPos-10, self.fractionDividerY], [xPos+10,self.fractionDividerY], 3)
        draw_text(str(denominator), self.font, (0,0,0), self.screen, xPos, self.denominatorY)

    def drawFractionMixed(self,leadco,numerator,denominator,xPos):
        if (numerator != 0):
            draw_text(str(leadco), self.font, (0,0,0), self.screen, xPos - 20, self.fractionDividerY)
            draw_text(str(numerator), self.font, (0,0,0), self.screen, xPos, self.numeratorY)
            pygame.draw.line(self.screen,colors.BLACK, [xPos-10, self.fractionDividerY], [xPos+10,self.fractionDividerY], 3)
            draw_text(str(denominator), self.font, (0,0,0), self.screen, xPos, self.denominatorY)
        else:
            draw_text(str(leadco), self.font, (0,0,0), self.screen, xPos - 20, self.fractionDividerY)

    # draw all fractions and symbols between fractions for current problem+answer
    def draw(self):
        if (self.stateManager.getCurrentState() != "Finished"): # only draw two problem fractions and x symbol
            draw_text(self.operationSymbol,self.font,(0,0,0),self.screen,self.xMid,self.yDraw)
            self.drawFraction(self.numerator1,self.denominator1,self.xMid - self.xOffset)
            self.drawFraction(self.numerator2,self.denominator2,self.xMid + self.xOffset)
            if (self.stateManager.getCurrentState() == "Shading Horizontally"):
                self.userdenominator = self.stateManager.get_answerDenom()
        elif (self.stateManager.getCurrentState() == "Finished"):
            if self.stateManager.operation_type == 2 or self.stateManager.operation_type == 4: # division or addition
                self.userdenominator = self.stateManager.get_answerDenom()
                print("Addition here")
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
            elif userAnswer.canReduce() == True and cpuAnswer.canReduce() == True:
                canreduce = True
                cpucanreduce = True
            else:
                pass
                # userAnswer.denominator = cpuAnswer.denominator


            if canreduce == True or cpucanreduce == True: # user answer can be reduced so theres 7 total symbols
                userAnswerReduced = Fraction(userAnswer.getNum(),userAnswer.getDenom())
                userAnswerReduced.finalReduce()
                cpuAnswerReduced = Fraction(cpuAnswer.getNum(),cpuAnswer.getDenom())
                cpuAnswerReduced.finalReduce()
                # if user num and denom match known problem num and denom they got it right -> set isEqualSymbol to =
                if userAnswerReduced.getNum() == cpuAnswerReduced.getNum() and userAnswerReduced.getDenom() == cpuAnswerReduced.getDenom():
                    isEqualSymbol = '='
                    self.hasRightAnswer = True
                else:
                    isEqualSymbol = '=/='
                    self.hasRightAnswer = False
                draw_text(isEqualSymbol,self.font,(0,0,0),self.screen,self.xMid,self.yDraw)
                #draw stuff from left of equal sign moving left
                self.drawFraction(self.numerator2,self.denominator2,self.xMid - self.xOffset)
                draw_text(self.operationSymbol,self.font,(0,0,0),self.screen,self.xMid- self.xOffset * 2,self.yDraw)
                self.drawFraction(self.numerator1,self.denominator1,self.xMid - self.xOffset*3)
                #draw stuff from right of equal sign moving right
                self.drawFraction(userAnswer.getNum(),userAnswer.getDenom(),self.xMid + self.xOffset)
                draw_text('=', self.font, (0,0,0),self.screen,self.xMid + self.xOffset * 2,self.yDraw)
                userAnswerReduced.finalReduce()
                self.drawFraction(userAnswerReduced.getNum(),userAnswerReduced.getDenom(),self.xMid + self.xOffset * 3)
                if self.hasRightAnswer: # draw checkmark
                    self.drawSprite(self.checkmark,True)
                else:
                    self.drawSprite(self.x,True) # draw x b/c user wrong
            elif ismixed == True or cpuismixed == True: # user answer is a mixed fraction so there will be 6 symbols
                if userAnswer.getNum() == cpuAnswer.getNum() and userAnswer.getDenom() == cpuAnswer.getDenom() and userAnswer.getLeadC() == cpuAnswer.getLeadC():
                    isEqualSymbol = '='
                    self.hasRightAnswer = True
                else:
                    isEqualSymbol = '=/='
                    self.hasRightAnswer = False
                #left side
                self.drawFraction(self.numerator2,self.denominator2,self.xMid - self.xOffset)
                draw_text(self.operationSymbol,self.font,(0,0,0),self.screen,self.xMid- self.xOffset * 2,self.yDraw)
                self.drawFraction(self.numerator1,self.denominator1,self.xMid - self.xOffset*3)
                #right side
                draw_text(isEqualSymbol,self.font,(0,0,0),self.screen,self.xMid,self.yDraw)
                self.drawFractionMixed(userAnswer.getLeadC(),userAnswer.getNum(),userAnswer.getDenom(),self.xMid + self.xOffset)
                if self.hasRightAnswer: # draw checkmark
                   self.drawSprite(self.checkmark,False)
                else:
                   self.drawSprite(self.x, False) # draw x because user wrng
            else: #canreduce = False so there will be 5 symbols
                if userAnswer.getNum() == self.numeratorAnswer and userAnswer.getDenom() == self.denominatorAnswer:
                    isEqualSymbol = '='
                    self.hasRightAnswer = True
                else:
                    isEqualSymbol = '=/='
                    self.hasRightAnswer = False
                self.drawFraction(self.numerator2,self.denominator2,self.xMid) # draw problem fraction 2 1st because itll be in middle
                draw_text(self.operationSymbol,self.font,(0,0,0),self.screen,self.xMid- self.xOffset,self.yDraw)
                self.drawFraction(self.numerator1,self.denominator1,self.xMid - self.xOffset * 2)
                draw_text(isEqualSymbol,self.font,(0,0,0),self.screen,self.xMid + self.xOffset,self.yDraw)
                self.drawFraction(userAnswer.getNum(),userAnswer.getDenom(),self.xMid + self.xOffset * 2)
                if self.hasRightAnswer: # draw checkmark
                    self.drawSprite(self.checkmark,False)
                else:
                    self.drawSprite(self.x, False) # draw x because user wrng

    def drawSprite(self,sprite,isReduced): # isReduced param affects x offset of image drawn
        if isReduced == True:
            self.screen.blit(sprite,(self.xMid + self.xOffset * 4 - 10,self.yDraw - 30))
        else:
            self.screen.blit(sprite,(self.xMid + self.xOffset * 3 - 10,self.yDraw - 30))
    # this function called by problemGenerator class in getProblem method
    def setProblem(self,n1,d1,n2,d2,nAnswer,dAnswer):
        self.numerator1 = n1
        self.denominator1 = d1
        self.numerator2 = n2
        self.denominator2 = d2
        self.numeratorAnswer = nAnswer
        self.denominatorAnswer = dAnswer

                    
