#!/usr/bin/python3
import sys

# Simple Python (SPY) v2
# An interepreter for a primitive language 
# based on Python
# 
# Author: Basil Labib
# Date: Feb 17th, 2022'

# internal memory register
DATA = []
# garbage memory
GARBAGE = []

# Few notable language features
# 1. Tried to mimic Python language rules as much as possible
# 2. Boolean is stored as string in DATA as 0,1 are truthy in Python

#
# HELPER FUNCTIONS
#

def readFile(name):
  # return a list of list of tokens
  with open(name) as f:
    raw = f.readlines()
  return [line.split() for line in raw]

def find(memory, elem):
  # Returns: tuple having two elements
  # first element boolean (T/F)
  # second element int (index)
  idx = (False, None)
  for v in memory:
    if v == elem:
      # note: this will only check for first appearance of elem
      idx = (True, memory.index(v))
  return idx

def findRef(memory, var):
  idx = (False, None)
  for elem in memory:
    if isinstance(elem, tuple):
      if var == elem[0]:
        idx = (True, elem[1])
  return idx

def findVar(memory, var):
  idx = (False, None)
  for elem in memory:
    if isinstance(elem, tuple):
      if var == elem[0]:
        val = memory.index(elem)
        idx = (True, val)
  return idx

def getValue(term):
  if not term.isdigit():
    if findVar(DATA, term)[0]:
      value = DATA[findRef(DATA, term)[1]]
    else:
      print("Error: Attempt to use unintialized variable")
      sys.exit()
  else:
    value = int(term)
  return value

def getBoolean(value):
  return value == 'True'

def dumpCore(DATA):
  """
  Debugging function to dump DATA list
  Also, collects all garbage values and prints them
  """
  print(DATA)
  print("="*20)
  
  for elem in DATA:
    if isinstance(elem, tuple):
      print('VARIABLE: ', elem[0], DATA[elem[1]])
  
  # garbage
  for elem in DATA:
    if not isinstance(elem, tuple):
      found = False
      for ele in DATA:
        if isinstance(ele, tuple):
          if ele[1] == DATA.index(elem):
            found = True
      if not found:
        GARBAGE.append(elem)
  
  for elem in GARBAGE: print("GARBAGE: ", elem)
  
#
# HELPER FUNCTIONS ENDS
#

def assign(variable, value, type):
  """
  Simply assign value to variable based on type
  Quirks/Notable features:
  1. For literals (type = bool and num), assign() does not modify value
  2. For variables, it performs a reference lookup in DATA list and assigns the reference

  assign() handles 4 cases:
  1. Creation of new value and assignment to new variable
  a = 10
  
  2. Creation of new value but reassignment to old variable
  a = 3
  a = 12

  3. Reassignment of value reference to new variable
  a = 12
  b = 12

  4. Reassignment of value reference to old variable
  a = 12
  b = 10
  a = 10
  """
  if type == 'var':
    index = findRef(DATA, value)
    varIdx = findVar(DATA, variable)
    if index[0]:
      if varIdx[0]:
          # reassignment to variable
        DATA[varIdx[1]] = (variable, index[1])
      else:
          # new variable assigment
        DATA.append((variable, index[1]))
    else:
      print("Error: Attempt to assign uninitialized variable")
      sys.exit()

  elif type == 'num':
    index = find(DATA, value)
    varIdx = findVar(DATA, variable)
    if index[0]:
      if varIdx[0]:
        DATA[varIdx[1]] = (variable, index[1])
      else:
        DATA.append((variable, index[1]))
    else:
      if varIdx[0]:
        DATA.append(value)
        idx = DATA.index(value)
        DATA[varIdx[1]] = (variable, idx)
      else:
        DATA.append(value)
        idx = DATA.index(value)
        DATA.append((variable, idx))
  
  elif type == 'bool':
    index = find(DATA, value)
    varIdx = findVar(DATA, variable)
    if index[0]:
      if varIdx[0]:
        DATA[varIdx[1]] = (variable, index[1])
      else:
        DATA.append((variable, index[1]))
    else:
      if varIdx[0]:
        DATA.append(value)
        idx = DATA.index(value)
        DATA[varIdx[1]] = (variable, idx)
      else:
        DATA.append(value)
        idx = DATA.index(value)
        DATA.append((variable, idx))
  

def unaryEval(operator, term):
  """
  Evaluate based on table below
  yes means it's a legal operation
  no means it's illegal

  yes/no means evaluate based on type of variable

         | numbers | bools | vars 
  -------|---------|-------|--------
  -      | yes     | no    | yes/no
  not    | no      | yes   | yes/no
  """
  
  if operator == '-':
    if term.isdigit():
      value = getValue(term)
      result = -1 * value
      return result
    elif term == 'True' or term == 'False':
      print("Error: Cannot use", operator, "on boolean")
      sys.exit()
    else:
      # NOTE: we are assuming the variabe referenced exists in memory
      # handle case when undeclared variable is used 
      value = DATA[findRef(DATA, term)[1]]
      if str(value).isdigit() or str(value).lstrip("-").isdigit():
        result = -1 * value
        return result
      else:
        print("Error: Cannot use", operator, "on boolean")
        sys.exit()
  elif operator == 'not':
    if term.isdigit():
      print("Error: Cannot use", operator, "on integers")
      sys.exit()
    elif term == 'True' or term == 'False':
      value = getBoolean(term)
      result = not value
      return str(result)
    else:
      # NOTE: we are assuming the variabe referenced exists in memory
      # handle case when undeclared variable is used 
      value = DATA[findRef(DATA, term)[1]]
      if str(value) == 'True' or str(value) == 'False':
        result = not getBoolean(value)
        return str(result)
      else:
        print("Error: Cannot use", operator, "on integers")
        sys.exit()
  
def binaryEval(operator, term1, term2):
  """
  Straight forward evaluation based on type of term1 and term2
  
  """
  if term1 == 'True' or term1 == 'False' or term2 == 'True' or term2 == 'False':
    if operator == 'and':
      result = term1 and term2
      return getBoolean(result)
    elif operator == 'or':
      result = term1 or term2
      return getBoolean(result)
  
  value1 = getValue(term1)
  value2 = getValue(term2)
  
  if operator == '+':
    result = value1 + value2
  elif operator == '-':
    result = value1 - value2
  elif operator == '*':
    result = value1 * value2
  elif operator == '/':
    result = value1 // value2
  elif operator == '<':
    result = value1 < value2
  elif operator == '>':
    result = value1 > value2
  elif operator == '<=':
    result = value1 <= value2
  elif operator == '>=':
    result = value1 >= value2
  elif operator == '!=':
    result = value1 != value2
  elif operator == '==':
    result = value1 == value2
  return result

def interpret(program):
  """
  Heart of the interpreter

  Tokenize each line
  And interpret based on length of expression list
  clumsy but works ;)

  """
  for line in program:
    expr = line[line.index('=') + 1:]
    variable = line[0]

    if len(expr) == 1:
      term = expr[0]
      if term == 'True' or term == 'False':
        assign(variable, term, type='bool')
      elif term.isdigit():
        assign(variable, int(term), type='num')
      else:
        assign(variable, term, type='var')

    elif len(expr) == 2:
      evaluatedValue = unaryEval(expr[0], expr[1])
      if str(evaluatedValue) == 'True' or str(evaluatedValue) == 'False':
        assign(variable, str(evaluatedValue), type='bool')
      else:
        assign(variable, evaluatedValue, type='num')

    elif len(expr) == 3:
      evaluatedValue = binaryEval(expr[1], expr[0], expr[2])
      assign(variable, evaluatedValue, type='num')
    else:
      print("Error: illegal statement at line", program.index(line)+1)
      sys.exit()

def main():
  if len(sys.argv) < 2:
    print("Error: No input file", file=sys.stderr)
    sys.exit()
  program = readFile(sys.argv[1])

  # remove all empty lines
  program = [line for line in program if len(line) > 0]
  # remove all lines that begin with # (as comments are ignored)
  program = [line for line in program if not line[0] == '#']

  interpret(program)
  dumpCore(DATA)

if __name__ == "__main__":
  main()