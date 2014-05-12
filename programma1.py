#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import codecs
import re
import nltk
from nltk import bigrams


def len_els(lst):
	tot = 0
	for i in lst:
		tot += len(i)
	return tot

def process_file(file_addr):
	print "# " + file_addr + ":"
	fileInput = codecs.open(file_addr, "r", "utf-8")
	raw = fileInput.read()
	sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	frasi = sent_tokenizer.tokenize(raw)
	
	
	#### Confronti i due testi sulla base delle seguenti informazioni statistiche:
	### il numero di token
	tokens = map(lambda frase: nltk.word_tokenize(frase), frasi)
	tokens = reduce(lambda frase, frase_succ: frase + frase_succ, tokens)
	print "Num. token:", len(tokens)
	
	
	
	### la lunghezza media dei token in termini di caratteri
	# (escludendo la punteggiatura)
	word = re.compile("[a-zA-Z]", re.I)
	t_senza_punt = filter(lambda i: word.search(i), tokens)
	print "Lung. media token:", len_els(t_senza_punt) * 1.0 / len(t_senza_punt) * 1.0
	
	
	
	### la lunghezza media delle frasi in termini di token
	print "Lung. media frasi:", len(tokens) * 1.0 / len(frasi) * 1.0
	
	
	
	### la grandezza del vocabolario del testo
	vocab = set(t_senza_punt)
	print "Vocab:", len(vocab)
	
	
	
	### la lunghezza media dei token del vocabolario in termini di caratteri (escludendo la punteggiatura)
	print "Lung. media vocab:", len_els(vocab) * 1.0 / len(vocab) * 1.0
	
	
	
	### la ricchezza lessicale
	### calcolata attraverso la Type Token Ratio (TTR) sui primi 2000 token di ogni corpus
	vocab_2000 = set(t_senza_punt[0:2000])
	print "TTR:", len(vocab_2000) * 1.0 / 2000.0
	
	
	
	### il rapporto tra Sostantivi e Verbi 
	### (indice che caratterizza variazioni di registro linguistico)
	tokensPOS = nltk.pos_tag(tokens)
	
	# dati presi dal nltk_data/taggers/universal_tagset/en-ptb.map
	# ADJ - adjectives
	ADJ = ['JJ', 'JJR', 'JJRJR', 'JJS']
	# ADV - adverbs
	ADV = ['RB', 'RBR', 'RBS', 'WRB']
	# NOUN - nouns (common and proper)
	NOUN = ['NN', 'NNP', 'NNPS', 'NNS', 'NP']
	# VERB - verbs (all tenses and modes)
	VERB = ['MD', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'VP']
	
	sost = filter(lambda i: i[1] in NOUN, tokensPOS)
	verbi = filter(lambda i: i[1] in VERB, tokensPOS)
	print "Sost. / Verbi:", len(sost) * 1.0 / len(verbi) * 1.0
	
	
	
	### la densità lessicale
	### calcolata come il rapporto tra il numero totale di occorrenze nel testo di 
	### Sostantivi, Verbi, Avverbi, Aggettivi
	s_v_a_a_POS = NOUN + VERB + ADV + ADJ
	sost_verb_etc = filter(lambda i: i[1] in s_v_a_a_POS, tokensPOS)
	
	### e il numero totale di parole nel testo 
	### (ad esclusione dei segni di punteggiatura marcati con POS "," "."):
	t_senza_punt_POS = filter(lambda i: i[1] not in [".", ","], tokensPOS)
	
	### (|Sostantivi|+|Verbi|+|Avverbi|+|Aggettivi|)/( TOT-( |.|+|,| ) ).
	print "densità lessicale:", len(sost_verb_etc) * 1.0 / len(t_senza_punt_POS) * 1.0



def main():
	if len(sys.argv) < 3:
		print "Usage:"
		print "\tprogramma1.py corpus1.txt corpus2.txt"
		return
	
	process_file(sys.argv[1])
	print ""
	process_file(sys.argv[2])
	print ""

main()
