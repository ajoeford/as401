#
#Reporting Module
#
import ajemodule
import pickle
from classes import *
from utility import *


def account_balance(acct_num, dbcon):
    """
    Summary: Takes TB account number, returns TB account balance
    Parameters: String acct_num
    returns: Int balance
    """
    db = DBManagerDatetime(dbcon)

    db.query("SELECT * FROM gl WHERE account=?",(acct_num,))
    je_pieces = db.fetchall()

    total = 0
    for piece in je_pieces:
        #tests debit/credit and makes credits negative for total
        if piece[4] == False:
            total -= int(piece[3])
        else:
            total += int(piece[3])

    return total

def view_balance_prompt(dbcon):
    """
    Prints TB account, description, and balance
    """

    account_query = int(raw_input("Enter Account #: "))

    #get account description
    acct_description = get_acct_description(account_query,dbcon)

    #account exists break
    if not acct_description:
        print("TB account not found.")

    else:
        #get account total
        acct_balance = account_balance(account_query,dbcon)

        print(str(account_query)+" "+acct_description+" "+decify(acct_balance))

def reporting_module(dbcon):
    running = True

    while running:
        print ""
        print "1) View Account Balance"
        print "2) View Account Detail"
        print "3) View TB"
        print "X) Back\n"

        user_input = raw_input("Enter Command: ")

        if user_input == "X" or user_input == "x":
            running = False

        elif user_input == "1":
            view_balance_prompt(dbcon)

        elif user_input == "2":
            pass

        elif user_input == "8":
            pass
