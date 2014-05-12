#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import codecs
import re
import math
import nltk
from nltk import bigrams


def count(lst):
	return [(i, lst.count(i)) for i in set(lst)]


def sort(lst):
	return sorted(lst, key=lambda x: x[1], reverse=True)


def txt_spaces(txt, n, only_text=False):
	spaces = " " * (n - len(txt))
	return txt + ((not only_text) * spaces)


def format_num(x, last=False):
	if type(x) is float:
		x = ("%.8f" % x)
	else:
		x = repr(x)
	return txt_spaces(x, 20, only_text=last)
	

def format_ngram(x):
	if type(x) is tuple:
		if len(x) == 2:
			txt = "<'" + x[0] + "', '" + x[1] + "'>"
		else:
			txt = "<'" + x[0] + "', '" + x[1] + "', '" + x[2] + "'>"
	else:
		if x == '-':
			txt = x
		else:
			txt = "'" + x + "'"
	
	return txt_spaces(txt, 40)


def tabular_print(list1, list2=None):
	if list2:
		t1, t2 = sys.argv[1] + ":", sys.argv[2] + ":"
		print txt_spaces(t1, 60) + t2
	else:
		list2 = [False for i in list1]
	
	for i in map(None, list1, list2):
		if i[0]:
			key1, val1 = i[0][0], i[0][1] 
			txt = format_ngram(key1)
			txt += format_num(val1)
		else:
			txt += txt_spaces(repr(None), 60)
		
		if i[1]:
			key2, val2 = i[1][0], i[1][1]
			txt += format_ngram(key2)
			txt += format_num(val2, last=True)
		
		print txt


def interactive_print(txt, lst):
	if len(sys.argv) >= 4:
		print txt
		tabular_print(lst)
		print ""
	else:
		print txt.replace(":", "...")


def process_file(file_addr):
	print "# " + file_addr + ":"
	fileInput = codecs.open(file_addr, "r", "utf-8")
	raw = fileInput.read()
	sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	frasi = sent_tokenizer.tokenize(raw)
	
	tokens = map(lambda frase: nltk.word_tokenize(frase), frasi)
	tokens = reduce(lambda frase, frase_succ: frase + frase_succ, tokens)
	
	# return
	lists = []
	txts = []
	
	
	#### estraete ed ordinate in ordine di frequenza decrescente, indicando anche la relativa frequenza:
	
	### i 20 token più frequenti
	### escludendo la punteggiatura;
	word = re.compile("[a-zA-Z]", re.I)
	t_senza_punt = filter(lambda i: word.search(i), tokens)
	
	tmp = sort( count(t_senza_punt) )
	
	txts += ["I token più frequenti:"]
	lists += [tmp[0:20]]
	interactive_print(txts[-1], lists[-1])
	
	freq_token = dict(tmp)
	
	
	### le 10 PoS più frequenti (Part-of-Speech);
	tokensPOS = nltk.pos_tag(tokens)
	pos_types = [i[1] for i in tokensPOS]
	
	tmp = sort( count(pos_types) )
	
	txts += ["PoS più frequenti:"]
	lists += [tmp[0:10]]
	interactive_print(txts[-1], lists[-1])
	
	
	### i 10 trigrammi di token più frequenti
	trig = nltk.trigrams(tokensPOS)
	for i in range(3):
		### che non contengono punteggiatura e congiunzioni 
		trig = [j for j in trig if word.search(j[i][0]) and j[i][1] != "CC"]
		### e dove ogni token deve avere una frequenza maggiore di 2;
		trig = [j for j in trig if freq_token[ j[i][0] ] > 2]
	
	# rimuove PoS
	trig = [(i[0][0], i[1][0], i[2][0]) for i in trig]
	tmp = sort( count(trig) )
	
	txts += ["Trigrammi più frequenti:"]
	lists += [tmp[0:10]]
	interactive_print(txts[-1], lists[-1])
	
	
	
	#### estraete ed ordinate i 10 bigrammi
	
	bigr = nltk.bigrams(tokensPOS)
	for i in range(2):
		### che non contengono la punteggiatura, le congiunzioni e le preposizioni
		bigr = [j for j in bigr if word.search(j[i][0]) and j[i][1] not in ["CC", "IN"]]
		### e dove ogni token deve avere una frequenza maggiore di 2:
		bigr = [j for j in bigr if freq_token[ j[i][0] ] > 2]
	
	# rimuove PoS
	bigr = [(i[0][0], i[1][0]) for i in bigr]
	
	# F_osservata(<u,v>)
	tmp = sort( count(bigr) )
	freq_osserv_bigr = dict(tmp)
	
	#txts += ["Bigrammi più frequenti (freq osservata):"]
	#lists += [tmp[0:10]]
	#interactive_print(txts[-1], lists[-1])
	
	# F_attesa(<u,v>) = F(u) * F(v) / N
	tmp = [(i, freq_token[i[0]] * freq_token[i[1]] * 1.0 / len(bigr) * 1.0) for i in set(bigr)]
	tmp = sort(tmp)
	freq_attesa_bigr = dict(tmp)
	
	#txts += ["Bigrammi più frequenti (freq attesa):"]
	#lists += [tmp[0:10]]
	#interactive_print(txts[-1], lists[-1])
	
	
	### con probabilità congiunta massima, indicando anche la relativa probabilità;
	# P(<u,v>) = F(<u,v>) / N
	tmp = [(i, freq_osserv_bigr[i] * 1.0 / len(bigr) * 1.0) for i in set(bigr)]
	tmp = sort(tmp)
	
	txts += ["Bigrammi più probabili (prob congiunta):"]
	lists += [tmp[0:10]]
	interactive_print(txts[-1], lists[-1])
	
	prob_bigr = dict(tmp)
	
	
	### con probabilità condizionata massima, indicando anche la relativa probabilità;
	# P_cond(<u,v>) = F_attesa(<u, v) / N
	tmp = [(i, freq_attesa_bigr[i] * 1.0 / len(bigr) * 1.0) for i in set(bigr)]
	tmp = sort(tmp)
	
	txts += ["Bigrammi più probabili (prob condizionata):"]
	lists += [tmp[0:10]]
	interactive_print(txts[-1], lists[-1])
	
	prob_cond = dict(tmp)
	
	
	# Mutual Information (extra)
	# MI = log2( F(<u,v>) * N / F(u) * F(v) )
	tmp = [(i, math.log(freq_osserv_bigr[i]/freq_attesa_bigr[i], 2)) for i in set(bigr)]
	tmp = sort(tmp)
	
	txts += ["Bigrammi più associati (Mutual Information):"]
	lists += [tmp[0:10]]
	interactive_print(txts[-1], lists[-1])
	
	
	### con forza associativa massima (calcolata in termini di Local Mutual Information), indicando anche la relativa forza associativa;
	# LMI = F(<u,v>) * MI
	tmp = [(i, freq_osserv_bigr[i] * math.log(freq_osserv_bigr[i]/freq_attesa_bigr[i], 2)) for i in set(bigr)]
	tmp = sort(tmp)
	
	txts += ["Bigrammi più associati (Local Mutual Information):"]
	lists += [tmp[0:10]]
	interactive_print(txts[-1], lists[-1])
	
	
	
	#### dopo aver individuato e classificato le Entità Nominate (NE) presenti nel testo, estraete:
	NE = nltk.ne_chunk(tokensPOS)
	trees = filter(lambda i: type(i) is nltk.Tree, NE)
	
	
	### i 20 nomi propri di persona più frequenti (tipi), ordinati per frequenza;
	persone = filter(lambda i: i.node == "PERSON", trees)
	
	# [[('Satoru', 'NNP'), ('Iwata', 'NNP')], [('Mr.', 'NNP'), ('Iwata', 'NNP')], ...] 
	# -> ['Satoru Iwata', 'Mr. Iwata', ...]
	persone = [map(lambda tupla: tupla[0], nomi_POS) for nomi_POS in persone]
	persone = [reduce(lambda x, y: x + " " + y, nomi) for nomi in persone]
	
	tmp = sort( count(persone) )
	tmp += [("-", 0) for i in range(len(tmp), 20)]
	
	txts += ["Nomi di persona più frequenti:"]
	lists += [tmp[0:20]]
	interactive_print(txts[-1], lists[-1])
	
	
	### i 20 nomi propri di luogo più frequenti (tipi), ordinati per frequenza.
	luoghi = filter(lambda i: i.node == "GPE", trees)
	luoghi = [map(lambda tupla: tupla[0], nomi_POS) for nomi_POS in luoghi]
	luoghi = [reduce(lambda x, y: x + " " + y, nomi) for nomi in luoghi]
	
	tmp = sort( count(luoghi) )
	tmp += [("-", 0) for i in range(len(tmp), 20)]
	
	txts += ["Nomi di luogo più frequenti:"]
	lists += [tmp[0:20]]
	interactive_print(txts[-1], lists[-1])
	
	return lists, txts


def main():
	if len(sys.argv) < 3:
		print "Usage:"
		print "\tprogramma2.py corpus1.txt corpus2.txt [no_columns]"
		return
	
	lists1, txts = process_file(sys.argv[1])
	print ""
	lists2, txts = process_file(sys.argv[2])
	print ""
	
	if len(sys.argv) == 3:
		for i in range(len(txts)):
			print txts[i]
			tabular_print(lists1[i], lists2[i])
			print ""

main()
