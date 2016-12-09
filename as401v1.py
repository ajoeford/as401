#Accounting application

from decimal import *
import pickle
import sqlite3
from classes import *
from ajemodule import *
from chart import *

dbcon = sqlite3.connect('chart.db')


print("")
print("wlecome to AS401")
print("the premier accounting softwre for businesses.")

running = True

#global variables
chart_of_accounts = []
gl = []
je_list = []
aje_count = 1


def Main(dbcon):
    global running
    print "1) J/E Module"
    print "2) View J/E"
    print "3) Chart of Accounts"
    print "X) Exit\n"

    user_input = raw_input("Enter command: ")

    if user_input == "X":
        print "Goodbye\n"
        running = False
        dbcon.close()
    elif user_input == '1':
        aje_module(dbcon)
    elif user_input == '3':
        chart_module(dbcon)

while running:

    Main(dbcon)
