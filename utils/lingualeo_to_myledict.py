# -*- coding: utf-8 -*-

INPUT_FILE = 'lingueleo_dict.txt'
OUTPUT_FILE = 'myLE_dict.json'


def WriteLine(line, fOut):
    line = line.translate(None, '\n\r[]')
    line = line.replace('"', '\\"')
    entry = line.split('\t')
    fOut.write('\t["' + entry[1] + '",\t"' + entry[2] + '",\t"' + entry[3] + '"]')


def WriteFile(fIn, fOut):
    prevLine = ''
    for line in fIn:
        if prevLine != '':
            WriteLine(prevLine, fOut)
            fOut.write(',\n')
        prevLine = line
    WriteLine(prevLine, fOut)
    fOut.write('\n')

fIn = open(INPUT_FILE, 'r')

fOut = open(OUTPUT_FILE, 'w')
fOut.write('[\n')
WriteFile(fIn, fOut)
fOut.write(']')
