#
#Reporting Module
#
import ajemodule
import pickle
from classes import *
from ajemodule import get_acct_description


def account_balance(acct_num):
    """
    Summary: Takes TB account number, returns TB account balance
    Parameters: String acct_num
    returns: Int balance
    """

    #test if account exists now or in prompt function?

def view_balance_prompt(dbcon):
    """
    Prints TB account, description, and balance
    """

    dbcur = dbcon.cursor()

    je_query = int(raw_input("Lookup JE by #: "))

    dbcur.execute("SELECT * FROM gl WHERE je_number=?",(je_query,))
    je_pieces = dbcur.fetchall()

    if je_pieces:
        print("")
        print("JE "+str(je_pieces[0][3])+": " + je_pieces[0][4])
        for piece in je_pieces:
            print_piece(piece, dbcur)
    else:
        print("JE# not found.")

    dbcur.close()

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
            pass

        elif user_input == "2":
            pass

        elif user_input == "8":
            pass
