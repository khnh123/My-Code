import time
import re
def isTimeFormat(line,):
    try:
        time.strptime(line, '%M:%S') #works only %M till 60
        return True
    except ValueError:
        #output.append(line)
        return False
    
def t(line):
    if re.search(r'(\d+:\d+)', line) == None:
        return True
    else:
        #output.add(line)
        return False
    
f = open('input.txt', mode='r', encoding='utf-8-sig').read().split("\n")
output = []

string = '"'
for line in f:
    #print(isTimeFormat(line))
    #print(t(line))
    if (t(line) == True):
        string = string + " " + line
    #if (isTimeFormat(line) == False):
        #print(isTimeFormat(line), line)
        #string = string + line
    #if (isTimeFormat(line) == False) and (t(line)== False):
      #  string = string + line
    #else:
        
    
#for item in output:
#   string = string + item + " "
print(string + '"')

#print(len(f)
"""
if (isTimeFormat(f[0]) != True) and (t(f[0]) != True):
    pass #if f[0] == time 99:99
else:
    i = len(f) - 1
    while i >= 0:
        #print(f[i])
        del f[i]
        i = i - 2
string2 = ""
for item in output:
    string2 = string2 + item + " "     
print(*f )
#for line in f:
    #print(isTimeFormat(line))
    #print(re.search(r'(\d+:\d+)', line))
    #string = string + " " + str(isTimeFormat(line))
    #isTimeFormat(line)

#print(string)
#print(*output)
#f = open("input1.txt", "w",encoding='utf-8-sig')
#f.write(string)
#f.close()
#f.write(string)
#f.write("\n".join(str(item) for item in output))

#print(string2)
#f.write(string2)
#f.close()

#open and read the file after the appending:
#f = open("input.txt", "r")
#print(f.read())
"""
