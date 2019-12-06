import numpy as np
import sys
import re
import random
import math

class MGen:
    def __init__(self,file):
        self.filename = file
        self.dict = {}

        # process file
        path = os.getcwd()
        filename = file
        raw_text = open(filename, 'r', encoding='utf-8').read()
        print("Text is {} characters long".format(len(raw_text)))
        raw_text = raw_text.lower()

        words = [w for w in re.findall(r'\w+|[?.,!]', raw_text) if w.strip() != '' or w == '\n']
        print('Corpus length in words:', len(words))
        dict = {}
        for i in range(0,len(words)-1):
            if len(words[i]) < 20:
                expandDict(self.dict,words[i],words[i+1])
        # dict_keys is a list of keys
        
        self.dict_keys = getList(self.dict)
        print('Corpus length in dictionary:', len(self.dict))
        #first_words is a list of words that appear right after punctuations ,.?!
        self.first_words, self.first_long_words = getFirstList(self.dict)

def getList(dictionary):
    dict_list = []
    for key in dictionary.keys():
        dict_list.append(key)
    return dict_list

def getFirstList(dictionary):
    first_list = []
    long_list = []
    # l is the list of words that comes right after these punctuations
    l = dictionary['.'] + dictionary[','] + dictionary['?'] + dictionary['!']
    for key in l:
        first_list.append(key)
        if len(key) > 10:
            long_list.append(key)
    return first_list, long_list

def expandDict(dictionary,key,value):
    if key not in dictionary:
        dictionary[key] = []
    if len(value) < 15:
        dictionary[key].append(value)

def getNextProb(list):
    prob_dict = {}
    list_length = len(list)
    for item in list:
        prob_dict[item] = prob_dict.get(item, 0) + 1
    for key, value in prob_dict.items():
        prob_dict[key] = value / list_length
    return prob_dict

def numToString(num):
    nums = {'0':'zero',
            '1':'one',
            '2':'two',
            '3':'three',
            '4':'four',
            '5':'five',
            '6':'six',
            '7':'seven',
            '8':'eight',
            '9':'nine'}
    return nums[str(num)]

def nextWord(dict,prev_word,word_length):
    prob_list = getNextProb(dict[prev_word])
    highest_prob = 0
    next_word = ""
    #only leave the ones with exact word_length
    if word_length == 0:
        for i in prob_list:
            if len(i) > 9:
                if (prob_list[i] > highest_prob):
                    next_word = i
                    highest_prob = prob_list[i]
    elif word_length == 1:
        next_word = random.choice(['a','i'])
    else:
        for i in prob_list:
            if len(i) == word_length:
                rand = random.random()
                if rand < 0.01:
                    next_word = i
                    highest_prob = prob_list[i]
                    break
                elif prob_list[i] > highest_prob:
                    next_word = i
                    highest_prob = prob_list[i]
    if next_word == "":
        next_word = numToString(word_length)
    return next_word

def genSeq(fname, num):
    mg = MGen(fname)
    seq = ''
    choice = random.choice(mg.first_words)
    for i in range(1,len(num)+1):
        number = int(num[i-1])
        # deals with the first word
        if i == 1:
            if number == 0:
                choice = random.choice(mg.first_long_words)
            elif number == 1:
                choice = 'i'
            else:
                while (len(choice) != number):
                    choice = random.choice(mg.first_words)
            seq = choice
        # deals with the rest
        else: 
            choice = nextWord(mg.dict,choice,number)
            seq = seq + " " + choice
    return seq