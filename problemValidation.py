from fractionHandler import Fraction


MULTIPLICATION = 0
ADDITION = 1
SUBTRACTION = 2
DIVISION = 3

def isValidProblem(n1,d1,n2,d2,operationType):
  if operationType == MULTIPLICATION:
    return isValidProblemMultx(n1,d1,n2,d2)
  elif operationType == SUBTRACTION:
    return isValidProblemSubtract(n1,d1,n2,d2)
  elif operationType == DIVISION:
    return isValidProblemDiv(n1,d1,n2,d2)

def isValidProblemMultx(n1,d1,n2,d2):
  # do not allow problem to continue b/c one of 2 input fractions is mixed
  if (n1 > d1 or n2 > d2):
    return "For multiplication, numerator must be larger than its corresponding denominator"
  return True

def isValidProblemSubtract(n1,d1,n2,d2):
  if (n1 > d1 or n2 > d2):
    return "For subtraction, numerator must be larger than its corresponding denominator"
  f1 = Fraction(n1,d1)
  nA, dA = f1.fSub(n2,d2)
  if nA < 0:
    return "For subtraction, the answer must be greater than zero"
  return True

def isValidProblemDiv(n1,d1,n2,d2):
  if d1 == 0 or d2 == 0:
    return "For division, the denominator of each fraction must be greater than 1"
  if (n1 > d1 or n2 > d2):
    return "For division, numerator must be less than its corresponding denominator"
  nAns = n1 * d2
  dAns = d1 * n2
  ans = nAns / dAns
  if ans >= 2:
    return "Answer is too large. For division, the answer must be less than 2"
  return True
