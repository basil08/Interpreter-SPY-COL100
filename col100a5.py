#!/usr/bin/python3
import sys

# Simple Python (SPY)
# An interepreter for a primitive language 
# based on Python
#
# Author: Basil Labib
# Date: Feb 14th, 2022'

def readFile(name):
  # return a list of list of tokens
  with open(name) as f:
    raw = f.readlines()
  return [line.split() for line in raw]

# internal memory register
DATA = []
# garbage memory
GARBAGE = []

BINARY_OPS = ['+', '-', '*', '/', '<', '>', '>=', '<=', '==', '!=', 'and', 'or']
UNARY_OPS = ['-', 'not']

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
  

def interpret(program):
  for line in program:
    expr = line[line.index('=') + 1:]
    variable = line[0]
    if len(expr) == 1:
      # parsing first type statments
      # variable = term
      # term := var, integer, true, false
      term = expr[0]
      if term == 'True' or term == 'False': # handle variable = boolean cases
        index = find(DATA, term)
        varIdx = findVar(DATA, variable)
        
        if index[0]:
          if varIdx[0]:
            # reassignment to variable
            DATA[varIdx[1]] = (variable, index[1])
          else:
            # new variable assigment
            DATA.append((variable, index[1]))
        else:
          if varIdx[0]:
            # assigment of new term to old var
            DATA.append(term)
            idx = DATA.index(term)
            DATA[varIdx[1]] = (variable, idx)
          else:
            # assigment of new term to new var
            DATA.append(term)
            idx = DATA.index(term)
            DATA.append((variable, idx))
      elif term.isdigit():  # handle variable = integer_constant cases
        index = find(DATA, term)
        varIdx = findVar(DATA, variable)

        if index[0]:
          if varIdx[0]:
            # reassignment to variable
            DATA[varIdx[1]] = (variable, index[1])
          else:
            # new variable assigment
            DATA.append((variable, index[1]))
        else:
          if varIdx[0]:
            # assigment of new term to old var
            DATA.append(int(term))
            idx = DATA.index(int(term))
            DATA[varIdx[1]] = (variable, idx)
          else:
            # assigment of new term to new var
            DATA.append(int(term))
            idx = DATA.index(int(term))
            DATA.append((variable, idx))
      else:     # handle variable = other_variable case
        index = findRef(DATA, term)
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
    elif len(expr) == 2:
      # variable = unary_op term
      pass
      # op = expr[0]
      # term = expr[1]
      
      # if not op in UNARY_OPS:
      #   print("Error: unknown operator", op)
      #   sys.exit()
      
      # if op == '-':
      #   # parse term
      #   if term == 'True' or term == 'False':
      #     print("Error: invalid expression. Cannot operate on bool")
      #     sys.exit()
      #   elif not term.isdigit():
      #     # This is me being plain lazy
      #     # b = - a is an invalid statement in my langauge uwu
      #     print("Error: cannot negate variables")
      #     sys.exit()
      #   else:
      #     index = find(DATA, term)
      #     varIdx = findVar(DATA, variable)

      #     if index[0]:
      #       DATA.append(-1 * int(term))
      #       idx = DATA.index(-1 * int(term))
      #       if varIdx[0]:
      #         DATA[varIdx[1]] = (variable, idx)
      #       else:
      #         DATA.append((variable, idx))
      #     else:
      #       if varIdx[0]:
      #         DATA.append(-1 * int(term))
      #         idx = DATA.index(-1 * int(term))
      #         DATA[varIdx[1]] = (variable, idx)        
    elif len(expr) == 3:
      # variable = term1 binary_operator term2
      pass
    else:
      print("Error: illegal statement at line", program.index(line)+1)
      sys.exit()
  
def dumpCore(DATA):

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