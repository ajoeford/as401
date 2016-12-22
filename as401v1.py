#Accounting application

from decimal import *
import pickle
import sqlite3
from classes import *
from ajemodule import *
from chart import *
from reporting import *

dbcon = 'chart.db'

print("")
print("wlecome to AS401")
print("the premier accounting softwre for businesses.")

running = True

def Main(dbcon):
    global running
    print "1) J/E Module"
    print "2) Reporting Module"
    print "3) Chart of Accounts"
    print "X) Exit\n"

    user_input = raw_input("Enter command: ")

    if user_input == "X":
        print "Goodbye\n"
        running = False
        #dbcon.close()  from previous use of dbcon
    elif user_input == '1':
        aje_module(dbcon)
    elif user_input == '2':
        reporting_module(dbcon)
    elif user_input == '3':
        chart_module(dbcon)

while running:

    Main(dbcon)
