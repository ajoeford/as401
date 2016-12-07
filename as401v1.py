#Accounting application

from decimal import *
import pickle
import sqlite3
from classes import *
from ajemodule import *

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

account_classification_list = {'A':'Asset','L':'Liability','OE':'Equity',
    'R':'Revenue','E':'Expense'}


def create_account(dbcur, dbcon):
    """Add an account to the TB"""
    global chart_of_accounts
    create_account_running = True

    while create_account_running:
        print ""
        print "CREATE ACCOUNT!!!"
        print ""

        num_loop = True
        while num_loop:
            print "Enter account number: "
            acct_num = raw_input(" ")

            for account in chart_of_accounts:
                if account.get_acct_num() == acct_num:
                    print "Account number already exists."
                    break
            else:
                num_loop = False

        print "Enter account name: "
        acct_name = raw_input(" ")

        acct_classification = ""
        while acct_classification not in ["A", "L", "OE", "R", "E"]:

            print "Enter account classification (A/L/OE/R/E)"
            acct_classification = raw_input(" ")

        acct_classification = account_classification_list[acct_classification]
        print acct_num + ' ' + acct_name
        print "Account Classification: " + acct_classification

        unaccepted = True
        while unaccepted:
            continue_prompt = raw_input("Is this correct? (Y/N) ")

            if continue_prompt == 'Y' or continue_prompt == 'y':
                new_account_tuple = (acct_num, acct_name, acct_classification)
                dbcur.execute("INSERT INTO chartofaccounts VALUES (?,?,?)", new_account_tuple)
                dbcon.commit()

                unaccepted = False
                create_account_running = False

            if continue_prompt == 'N':
                unaccepted = False

def edit_account(dbcur, dbcon):
    """Change account name or classification based on account number"""
    global chart_of_accounts
    valid_account = ""

    acct_input = raw_input("Enter account number: ")

    dbcur.execute("SELECT * FROM chartofaccounts WHERE num=?", (acct_input,))
    to_edit = dbcur.fetchone()

    if to_edit:
        print(to_edit[0]+" "+to_edit[1])
        print("Classification: "+to_edit[2])

        edited = False
        while edited == False:
            ask_name = raw_input("Edit account name? (Y/N) ")

            if ask_name == 'Y' or ask_name == 'y':
                new_name = raw_input("Enter new name: ")

                dbcur.execute("UPDATE chartofaccounts SET description=? WHERE num=?", (new_name,acct_input))
                dbcon.commit()
                edited = True

            ask_class = raw_input("Change account classification? (Y/N) ")

            if ask_class == 'Y' or ask_class == 'y':

                acct_classification = ""
                while acct_classification not in ["A", "L", "OE", "R", "E"]:

                    print "Enter account classification (A/L/OE/R/E)"
                    acct_classification = raw_input("Classification: ")
                acct_classification = account_classification_list[acct_classification]
                dbcur.execute("UPDATE chartofaccounts SET classification=? WHERE num=?", (acct_classification,acct_input))
                dbcon.commit()
                edited = True
    else:
        print("Invalid account number.")

def view_chart(dbcur):
    print ""

    dbcur.execute("SELECT * FROM chartofaccounts")
    all_chart = dbcur.fetchall()

    if all_chart:
        for acct in all_chart:
            print(acct[0]+" "+acct[1])
    else:
        print("No TB accounts.")

def delete_account(dbcur, dbcon):
    """Remove account from Chart of Accounts"""
    global chart_of_accounts
    to_delete = ""

    print("")
    delete_num = raw_input("Enter account number: ")

    dbcur.execute("SELECT * FROM chartofaccounts WHERE num=?", (delete_num,))
    to_delete = dbcur.fetchone()

    if to_delete:
        print("Are you sure you want to delete the following account?")
        print(to_delete[0] + " "+to_delete[1])

        affirm = raw_input("Delete? (Y/N) ")
        if affirm == 'Y' or affirm == 'y':
            dbcur.execute("DELETE FROM chartofaccounts WHERE num=?", (delete_num,))
            dbcon.commit()
    else:
        print("Invalid account number.")

def view_chart(dbcur):
    print ""

    dbcur.execute("SELECT * FROM chartofaccounts")
    all_chart = dbcur.fetchall()

    for acct in all_chart:
        print(acct[0]+" "+acct[1])

def initiate_chart_db(dbcur):

    dbcur.execute('''CREATE TABLE chartofaccounts
                    (num text, description text, classification text)''')

def chart_module(dbcon):
    global chart_of_accounts
    chart_running = True

    dbcur = dbcon.cursor()

    while chart_running:
        print ""
        print "TB Accounts Module"
        print ""

        print "1) Create New Account"
        print "2) Edit Existing Account"
        print "3) View Chart of Accounts"
        print "4) Delete Existing Account"
        print "5) Initiate Chart DB"
        print "X) Back\n"

        user_input = raw_input("Enter Command: ")

        if user_input == "X":
            chart_running = False

        elif user_input == "1":
            create_account(dbcur, dbcon)

        elif user_input == "2":
            edit_account(dbcur, dbcon)

        elif user_input == "3":
            view_chart(dbcur)

        elif user_input == "4":
            delete_account(dbcur, dbcon)

        elif user_input == "5":
            initiate_chart_db(dbcur)


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
