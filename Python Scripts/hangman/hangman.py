# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 20:27:24 2020

@author: George Zhou
"""
#hangman picturse
with(open('hangman.txt','r')) as f:
        hangMan=f.read().split(',')
        
#hangman wordbank 
with(open('wordbank.txt','r')) as f:
        wordBank=f.read().split('\n')    

from random import choice
from re import *

def wordModify(index,wordSTR,guess):
    charList=list(wordSTR)
    for i in index:
        charList[i]=guess
    return(''.join(charList))

def displayLetters(word,letters):
    lettersSort=sorted([i for i in letters if i not in word])
    if not lettersSort:
        return("")
    else:
        return(', '.join(lettersSort))
   
def hangman(wordList):
    message='Have fun!'
    limbs=0
    done=False
    #list for letters used
    lettersUsed=[]
    #make all letters lowercase 
    word = choice(wordList).lower()
    wordHyphen=sub('\w','-',word) #mask word
    while(done==False):
       print(message)
       print(hangMan[limbs]+'\n')
       print(wordHyphen)
       print('letters used: '+ displayLetters(word, lettersUsed)) #display letters nicely
       guess=input('Please guess a letter: ').lower()
       if len(guess)!=1 or guess.isalpha()==False:
           message="Please pick an appropriate letter."
           print("\n"*50)
       elif guess in lettersUsed:
           message='Please pick a letter that was not used before!'
           print("\n"*50)
       else:
            indices = [i for i, a in enumerate(word) if a == guess]
            if not indices:
                limbs+=1
                lettersUsed.append(guess)
                message='Have fun!'
                print("\n"*50)
                if limbs==6:
                    print("Sorry you lose! The phrase was: "+word)
                    print(hangMan[6]+'\n')
                    print(wordHyphen+'\n')
                    print('Please guess a letter: '+guess)
                    done=True
            else:
                #show letter position in word
                wordHyphen=wordModify(indices, wordHyphen, guess)
                lettersUsed.append(guess)
                print("\n"*50)
                if wordHyphen==word:
                    print('Congragulations, you won!')
                    print(hangMan[limbs]+'\n')
                    print(wordHyphen)
                    done=True
hangman(wordBank)
    