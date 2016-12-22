#Accounting application

from decimal import *
from classes import *
import pickle
import sqlite3

account_classification_list = {'A':'Asset','L':'Liability','OE':'Equity',
    'R':'Revenue','E':'Expense'}

def tb_account_exists(acct_num, dbcon):
    """Test to see if account already exists
        returns boolean"""

    db = DBManagerDatetime(dbcon)

    db.query("SELECT * FROM chartofaccounts WHERE num=?", (acct_num,))
    if db.fetchone():
        return True
    else:
        return False

def create_account(dbcon):
    """Add an account to the TB
    Makes change to DB through parameters:
    String dbcon: db name
    """

    db = DBManagerDatetime(dbcon)

    create_account_running = True

    while create_account_running:
        print ""
        print "CREATE ACCOUNT!!!"
        print ""

        num_loop = True
        while num_loop:
            print "Enter account number: "
            acct_num = raw_input(" ")

            if tb_account_exists(acct_num, dbcon) == False:
                num_loop = False
            else:
                print("Account number already exists.")

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
                db.query("INSERT INTO chartofaccounts VALUES (?,?,?)", new_account_tuple)

                unaccepted = False
                create_account_running = False

            if continue_prompt == 'N':
                unaccepted = False

def edit_account(dbcon):
    """Change account name or classification based on account number.
    String dbcon = db filename
    """
    valid_account = ""
    db = DBManagerDatetime(dbcon)

    acct_input = raw_input("Enter account number: ")

    db.query("SELECT * FROM chartofaccounts WHERE num=?", (acct_input,))
    to_edit = db.fetchone()

    if to_edit:
        print(to_edit[0]+" "+to_edit[1])
        print("Classification: "+to_edit[2])

        edited = False
        while edited == False:
            ask_name = raw_input("Edit account name? (Y/N) ")

            if ask_name == 'Y' or ask_name == 'y':
                new_name = raw_input("Enter new name: ")

                db.query("UPDATE chartofaccounts SET description=? WHERE num=?", (new_name,acct_input))
                edited = True

            ask_class = raw_input("Change account classification? (Y/N/eXit) ")

            if ask_class == 'Y' or ask_class == 'y':

                acct_classification = ""
                while acct_classification not in ["A", "L", "OE", "R", "E"]:

                    print "Enter account classification (A/L/OE/R/E)"
                    acct_classification = raw_input("Classification: ")
                acct_classification = account_classification_list[acct_classification]
                db.query("UPDATE chartofaccounts SET classification=? WHERE num=?", (acct_classification,acct_input))
                edited = True

            if ask_class == 'X':
                edited = True
    else:
        print("Invalid account number.")

def view_chart(dbcon):
    """prints all entries in chartofaccounts db
    probably should update this to return rather than straight print
    """
    db = DBManagerDatetime(dbcon)

    print ""

    db.query("SELECT * FROM chartofaccounts ORDER BY num")
    all_chart = db.fetchall()

    if all_chart:
        for acct in all_chart:
            print(acct[0]+" "+acct[1])
    else:
        print("No TB accounts.")

def delete_account(dbcon):
    """Remove account from Chart of Accounts.
    String dbcon = db filename
    """
    db = DBManagerDatetime(dbcon)
    to_delete = ""

    print("")
    delete_num = raw_input("Enter account number: ")

    db.query("SELECT * FROM chartofaccounts WHERE num=?", (delete_num,))
    to_delete = db.fetchone()

    if to_delete:
        print("Are you sure you want to delete the following account?")
        print(to_delete[0] + " "+to_delete[1])

        affirm = raw_input("Delete? (Y/N) ")
        if affirm == 'Y' or affirm == 'y':
            db.query("DELETE FROM chartofaccounts WHERE num=?", (delete_num,))
    else:
        print("Invalid account number.")

def initiate_chart_db(dbcon):
    """Creates table in DB for the chart of accounts.
    dbcon = db filename
    """
    db = DBManagerDatetime(dbcon)

    confirm = raw_input("Please enter admin password: ")

    if confirm == "saltedpork":
        db.query('''CREATE TABLE chartofaccounts
                        (num text, description text, classification text)''')
        print("Chart of accounts initiated.")

    else:
        print("Incorrect password.")

def chart_module(dbcon):
    """Menu loop for the Chart of Accounts module.
    dbcon = db connection from sqlite3"""
    chart_running = True

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
            create_account(dbcon)

        elif user_input == "2":
            edit_account(dbcon)

        elif user_input == "3":
            view_chart(dbcon)

        elif user_input == "4":
            delete_account(dbcon)

        elif user_input == "5":
            initiate_chart_db(dbcon)
