# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 20:27:24 2020

@author: George Zhou
"""
from random import choice
from re import *


#hangman picturse
with(open('hangman.txt','r')) as f:
        hangMan=f.read().split(',')
        
#hangman wordbank 
with(open('wordbank.txt','r')) as f:
        wordBank=f.read().split('\n')    

#modify hyphen structure
def wordModify(index,wordSTR,guess):
    charList=list(wordSTR)
    for i in index:
        charList[i]=guess
    return(''.join(charList))
#display letters used 
def displayLetters(word,letters):
    lettersSort=sorted([i for i in letters if i not in word])
    if not lettersSort:
        return("")
    else:
        return(', '.join(lettersSort))
#check if guess is valid 
def checkLetter(lettersUsed):  
    guess=input('Please guess a letter: ').lower()
    global message
    if len(guess)!=1 or guess.isalpha()==False:
          message="Please pick an appropriate letter."
          return('none',message)
    elif guess in lettersUsed:
        message='Please pick a letter that was not used before!'
        return('none',message)
    else:
        message='Have fun!'
        return(guess,message)
#check if guess is in word, and show results 
def indiceCheck(word,wordHyphen,guess,limbs,lettersUsed):
    indices = [i for i, a in enumerate(word) if a == guess]
    if not indices:
        limbs+=1
        lettersUsed.append(guess)
        print("\n"*50)
        return(lettersUsed,wordHyphen,limbs)
    else:
        wordHyphen=wordModify(indices, wordHyphen, guess)
        lettersUsed.append(guess)
        print("\n"*50)
        return(lettersUsed,wordHyphen,limbs)
#check if you win or lose 
def endGame(limbs,wordHyphen,word,guess):
    if limbs==6:
        print("Sorry you lose! The phrase was: "+word)
        print(hangMan[6]+'\n')
        print(wordHyphen+'\n')
        print('Please guess a letter: '+guess)
        return(True)
    elif word==wordHyphen:
        print('Congragulations, you won!')
        print(hangMan[limbs]+'\n')
        print(wordHyphen)
         
def hangman(wordList):
    limbs=0
    done=False
    message='Have fun!'
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
       guess,message=checkLetter(lettersUsed)
       if guess != 'none':
           lettersUsed,wordHyphen,limbs=indiceCheck(word, wordHyphen, guess, limbs, lettersUsed)
           if wordHyphen==word or limbs==6:
               done=endGame(limbs, wordHyphen,word,guess)

hangman(wordBank)
                   
