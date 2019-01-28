from __future__ import with_statement
import os
import re

COMPUTATIONS = {
  "0": "0101010",
  "1": "0111111",
  "-1": "0111010",
  "D": "0001100",
  "A": "0110000",
  "!D": "0001101",
  "!A": "0110001",
  "-D": "0001111",
  "-A": "0110011",
  "D+1": "0011111",
  "A+1": "0110111",
  "D-1": "0001110",
  "A-1": "0110010",
  "D+A": "0000010",
  "D-A": "0010011",
  "A-D": "0000111",
  "D&A": "0000000",
  "D|A": "0010101",
  "M": "1110000",
  "!M": "1110001",
  "-M": "1110011",
  "M+1": "1110111",
  "M-1": "1110010",
  "D+M": "1000010",
  "D-M": "1010011",
  "M-D": "1000111",
  "D&M": "1000000",
  "D|M": "1010101"
  }


DESTINATIONS = {
  "null": "000",
  "M": "001",
  "D": "010",
  "A": "100",
  "MD": "011",
  "AM": "101",
  "AD": "110",
  "AMD": "111"
  }


JUMP = {
  "null": "000",
  "JGT": "001",
  "JEQ": "010",
  "JGE": "011",
  "JLT": "100",
  "JNE": "101",
  "JLE": "110",
  "JMP": "111"
  }

table = {
  "SP": 0,
  "LCL": 1,
  "ARG": 2,
  "THIS": 3,
  "THAT": 4,
  "SCREEN": 16384,
  "KBD": 24576,
  }

for i in range(0,16):
  label = "R" + str(i)
  table[label] = i


variableCursor = 16    
root = 'pong.asm'     


def normalize(line):
  line1 = line
  if not "=" in line1:
    line1 = "null=" + line1
  if not ";" in line1:
    line1 = line1 + ";null"
  return line1


def addVariable(label):
  global variableCursor
  table[label] = variableCursor
  variableCursor += 1
  return table[label]


def aTranslate(line):
  if line[1].isalpha():
    label = line[1:-1]
    aValue = table.get(label, -1)
    if aValue == -1:
      aValue = addVariable(label)
  else:
    aValue = int(line[1:])
  bValue = bin(aValue)[2:].zfill(16)
  return bValue
 

def cTranslate(line):
  a = comp = dest = jump = ''
  #get jump portion and comp
  if ';' in line:
    #get index where the jmp begins
    index = line.find(';')
    #get jump type
    jumpName = line[index+1:len(line)-1]
    #see if there's an M in comp part
    if 'M' in line[:index]: a = '1'
    #get binary representation
    jump = JUMP[jumpName]
    compName = line[:index]
    comp = COMPUTATIONS[compName]

  elif '=' in line:
    #get index where dest begins
    index = line.find('=')
    #get destination type
    destName = line[0:index]
    compName = line[index+1:len(line)-1]
    #see if there's an M in comp part
    if 'M' in line[index:]: a = '1'
    #get binary representation
    comp = COMPUTATIONS[compName]
    
    dest = DESTINATIONS[destName]

  if not comp: comp = '0000000'
  if not dest: dest = '000'
  if not jump: jump = '000'
  if not a: a = '0'

  return (a, comp, dest, jump)

def translate(line):
  if line[0] == "@":
    return aTranslate(line)
  else:
    c = cTranslate(line)
    return "111" + c[1] + c[2] + c[3]


def firstPass():

  infile = open(root)
  outfile = open(root + ".tmp", "w")

  lineNumber = 0
  for line in infile:
    if line != "":
      if line[0] == "(":
        label = line[1:-1]
        table[label] = lineNumber
        line = ""
      else:
        lineNumber += 1
        outfile.write(line)
    line = line.strip() #strip space
    line = line.split('//')[0].strip() #strip comment
  outfile.write("\n")  

  infile.close()
  outfile.close()


def assemble():
  infile = open(root + ".tmp")
  outfile = open(root + ".hack", "w")

  for line in infile:
    tline = translate(line)
    outfile.write(tline + "\n")


  infile.close()
  outfile.close()
  os.remove(root + ".tmp")



firstPass()
assemble()


#testing 



'''
transFile = open('pong.asm.hack', "r").read()
hackFile = open('pong.hack',"r").read()
if transFile==hackFile:
  print("Success!")
  
'''

f1 = open('pong.asm.hack')
f2 = open('pong.hack')
lines1=f1.readlines()
lines2=f2.readlines()

n=0
while n<27483:
  if lines1[n]!=lines2[n]:
    print(lines1[n])
  n=n+1





#-----------------------------------
''' 
  a = comp = dest = jump = ''
  #get jump portion and comp
  if ';' in line:
    #get index where the jmp begins
    index = line.find(';')
    #get jump type
    jumpName = line[index+1:]
    #see if there's an M in comp part
    if 'M' in line[:index]: a = '1'
    #get binary representation
    jump = JUMP.get(jumpName)
    compName = line[:index]
    comp = COMPUTATIONS.get(compName)
  elif '=' in line:
    #get index where dest begins
    index = line.find('=')
    #get destination type
    destName = line[0:index]
    compName = line[index+1:]
    #see if there's an M in comp part
    if 'M' in line[index:]: a = '1'
    #get binary representation
    comp = self.getValueByName(compName, self.__m_Comps)
    dest = DESTINATIONS.get(destName)

  if not comp: comp = '0000000'
  if not dest: dest = '000'
  if not jump: jump = '000'
  if not a: a = '0'
  '''






"""
  if '=' in line:
    token = line.split('=')
    des = dest[token[0]]
    line = token[1]
 # else:
 #  des = dest['null']
 #  token = line.split(';')
 #  com = comp[token[0]]
  if ';' in line:
    jmp = jump[token[1]]
  else:
    jmp = jump['null']
    #"111"compdestjump
  return '''com''', des, jmp
"""
