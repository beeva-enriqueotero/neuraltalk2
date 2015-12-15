#!/usr/bin/env python

FPS=4.0
filename_in = 'subs_in.txt'
filename_out = 'subs.srt'

import sys
file_in = sys.stdin
#file_in = open(filename_in)


def myjacc(s1,s2):
    l1 = s1.split()
    l2 = s2.split()
    jaccard = len(set.intersection(set(l1),set(l2)))*1.0/len(set.union(set(l1),set(l2)))
    return jaccard

mylines = [line.rstrip('\n') for line in file_in]
mylines = map(lambda x:x.replace('\t',''),mylines)
file_in.close()

from itertools import groupby as g
def most_common_oneliner(L):
  return max(g(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))[0]

count = 0
gap = 0
lines = mylines[:]
mylist = []
for i in range(len(lines)-1):
    l1 = lines[i-0]
    l2 = lines[i+1]
    if l1 != "..." and myjacc(l1,l2) >= 0.5:
        count+=1
        mylist.append(l1)
    else:
        gap+=1
        if (gap > 2):
            count = 0
            gap = 0
            mylist = []
    mycommon = "..."
    if (mylist) and (count > 1):
        mycommon = most_common_oneliner(mylist)

    lines[i] = mycommon


file_out = sys.stdout
#file_out = open(filename_out,'w+')

import datetime
myinit = -1
myend = 0
mycount = 1
for i in range(len(lines)-1):
    if (lines[i] == lines[i+1]) and (myend >= 0):
        myinit = i
        myend == -1
    else:
        myend = i+1
        if (lines[i] != "..."):
            print >>file_out, mycount
            sinit = (myinit-2)/FPS
            send = (myend+2)/FPS
            timeinit = datetime.timedelta(seconds=sinit)
            timeend = datetime.timedelta(seconds=send)
            mystr = "0%s --> 0%s" %(timeinit,timeend)
            mystr = mystr.replace(".",",")
            print >>file_out, mystr
            print >>file_out, lines[i]+"\n"
            mycount +=1
file_out.close()
