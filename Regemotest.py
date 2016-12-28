# -*- coding: utf-8 -*-
from nltk.util import ngrams
import nltk
import codecs
import unicodedata
import operator
import re
import json
from os import listdir
from os.path import isfile, join
import sys
from multiprocessing import Process
from operator import itemgetter

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def sample_match(word_list):
	edges = {}
	chbigram=list2bigram(word_list)
	bigramfreqdict=bigram2freqdict(chbigram)
	bigramfreqsorted=sorted(bigramfreqdict.items(), key=itemgetter(1), reverse=True)
	#print bigramfreqsorted

	maxi = 0.0
	foundMax = 0
	for (token,num) in bigramfreqsorted:
		if len(token[0]) != 0 and len(token[1]) != 0:
			if token[0] == " ":
				w1 = "_blank_"
			else:
				w1 = token[0]
			if token[1] == " ":
				w2 = "_blank_"
			else:
				w2 = token[1]
			if not foundMax:
				foundMax = 1
				maxi = float(num)
			edges["%s\t%s"%(w1,w2)]=float(num)/float(maxi)
	return edges;
			

def list2freqdict(mylist):
	mydict=dict()
	for ch in mylist:
		mydict[ch]=mydict.get(ch,0)+1
	return mydict

def list2bigram(mylist):
	return [mylist[i:i+2] for i in range(0,len(mylist)-1)]

def bigram2freqdict(mybigram):
	mydict=dict()
	for (ch1,ch2) in mybigram:
		mydict[(ch1,ch2)]=mydict.get((ch1,ch2),0)+1
	return mydict
