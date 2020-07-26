# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from random import *

def dice_roll():
    done=False
    done1="Yes"
    done2=True
    rolls=[]
    while done==False:
        print('''Please pick a program
    
        1) Roll a dice
        2) Rolls count  
        3) End program
        ''')
    
        choice = input('Choice: ')
        print('\n')
        if choice=='3' or choice=="":
            done=True
            print('Thank you for using our program!')
        elif choice=='1':
            while done1 in ['Yes','Y','yes','y']:
                num=randint(1, 6)
                print('You rolled a: %d \n' % num)
                rolls.append(num)
                done1 = input('Roll again? (Yes/No): ')
                print('\n')
        elif choice=='2':
            while done2==True:
                print("You have rolled %d times!" % len(rolls))
                print('\n')
                print('1: %d times' % rolls.count(1))
                print('2: %d times' % rolls.count(2))
                print('3: %d times' % rolls.count(3))
                print('4: %d times' % rolls.count(4))
                print('5: %d times' % rolls.count(5))
                print('6: %d times' % rolls.count(6))
                
                done2=input("Press enter to continue...")
        else:
            print("Please pick a choice in the menu! \n")

dice_roll()