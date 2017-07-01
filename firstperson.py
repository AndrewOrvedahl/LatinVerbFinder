#!/usr/bin/env python3

import re
import sys
import subprocess
import csv
import time
import string

#Open a pipe to bash because os.system() calls /bin/sh, which in some distros
# is dash
def bash_call(cmd):
    subprocess.Popen(['/bin/bash', '-c', cmd]) 
    return

def filter_verb_candidates(text):

    infile = open(text, 'r')
    outfile = open('potential_verbs.csv', 'w')

    vb1p = re.compile(r'(\w+)((r)|(o)|(m)|(mus))$')
    #matches all words with a potential first person ending:
    #o, m, r, mus, mur, i
    nvb1p = re.compile(r'(\w+)((ur)|(ir)|(mini)|(om))')
    #matches words with r and m endings that can't be first person verbs

    nLines = 0
    table = str.maketrans({key: None for key in string.punctuation})
    for line in infile:  
        nLines+=1
        #remove punctuation from line
        line.translate(table)
        
        for word in line.split():
            if(vb1p.match(word) and not nvb1p.match(word)):
                output = word + ', ' + str(nLines) + '\n'
                outfile.write(output)
    infile.close()
    outfile.close()
    return
   
def call_words():
    
    with open('potential_verbs.csv', 'r') as source:
        infile = csv.reader(source)
        
        for row in infile:
            outfile = open('WWW.txt', 'a+')
            LineNumber = '** ' + str(row[-1])
            outfile.write('\n\n\n\n' + LineNumber + '\n')
            outfile.close

            cmd = 'words <<< \'' + row[0] + '\' >> ' + 'WWW.txt'
            bash_call(cmd)

            #WWW prints slower than a for loop iteration, so we need to wait
            time.sleep(0.01)
            
        source.close()
    return

def write_dictionary():
    
    infile = open('WWW.txt', 'r')
    outfile = open('verbs.txt', 'w')
    
    inDef = False
    dictionary = {}
    highestLine = 0
    seenBefore = False

    lineMatch = re.compile(r'(\*\*\s+)(\d+)')
    vbMatch = re.compile(
        r'(\s*\w+\.\w+\s+)(V)(\s+\d\s+\d\s+\w+\s+\w+\s+\w+\s+1\s+[SP]\s*)')  
    
    for line in infile:
        x = lineMatch.match(line)
        if(x and not inDef):
            inDef = True
            lineNum = int(x.group(2))
            continue
        y = vbMatch.match(line)
        if(inDef and y):
            if(not seenBefore):
                highestLine = lineNum
                seenBefore = True
                dictionary[str(highestLine)] = [y.group(1)]
            if(seenBefore):
                highestLine = lineNum
                dictionary[str(highestLine)].append(y.group(1))
                continue
        else:
            continue
    
    for k,v in dictionary.items():
        outfile.write(str(k)+'\n')
        for i in v:
            outfile.write(i + '\n')
        outfile.write('\n')
        
    infile.close()
    outfile.close()
    return

def clean_up():
    cmd = 'rm WWW.txt potential_verbs.csv'
    bash_call(cmd)
    return
    
def main(args):
    print('I made it to main!')
    
    text = args[1]

    #f = open('WWW.txt', 'w+')
    #f.close()
    
    filter_verb_candidates(text)
    print('Filtered candidates!')

    call_words()
    print('Called Words!')

    write_dictionary()
    print('Wrote the dictionary! Exiting.')

    try:
        if(args[2] == '--no_clean'):
            pass
        else:
            clean_up()
    except IndexError:
            clean_up()
    return

if __name__ == '__main__':
    print(sys.argv[1])
    if(len(sys.argv) < 2):
        print('Enter an input text!')
        sys.exit(1)
    else:
        main(sys.argv)
