#
#Reporting Module
#
import ajemodule
import pickle
from classes import *

def get_acct_description(acct_num, dbcur):
    #get account description
    dbcur.execute("SELECT description FROM chartofaccounts WHERE num=?", (acct_num,))
    return dbcur.fetchone()[0]

def create_aje(dbcon):
    """Make an AJE"""
    global gl
    global aje_count
    global je_list

    dbcur = dbcon.cursor()

    read_pkl = open('gldata.pkl', 'rb')
    aje_count = pickle.load(read_pkl)
    read_pkl.close()

    aje_lines_list = []

    print ""
    print "Journal Entry #" + str(aje_count)
    input_description = raw_input("Enter J/E description: ")

    aje_lines = 1
    aje_lines_loop = True
    while aje_lines_loop:
        print ""
        print "JE Line " + str(aje_lines) + ":"

        valid_account = False
        while valid_account == False:
            input_acct = raw_input("Enter account: ")

            if input_acct == 'X':
                break

            #test if account exists in TB
            if account_exists(input_acct, dbcur):
                valid_account = True
            else:
                print("TB Account does not exist.")


        input_value = raw_input("Enter amount: ")

        debit_loop = True
        while debit_loop:
            input_sign = raw_input("Debit or Credit? (D/C): ")
            if input_sign in ['D','d']:
                input_sign = 'Dr'
                debit_loop = False
            elif input_sign in ['C','c']:
                input_sign = 'Cr'
                debit_loop = False

        #confirmation of JE line
        updated_ajes = je_piece_loop(aje_lines_list, aje_lines, input_sign, input_acct, input_value,
                                    dbcur)
        aje_lines_list = updated_ajes[0]
        aje_lines = updated_ajes[1]

        #confirmation of full JE
        updated_confirm_loop = confirm_je_loop(aje_count, input_description, aje_lines_list, dbcon)
        aje_count = updated_confirm_loop[0]
        aje_lines_loop = updated_confirm_loop[1]

        #write new aje_count to file
        pkl_cursor = open('gldata.pkl', 'wb')
        pickle.dump(aje_count, pkl_cursor)
        pkl_cursor.close()

def print_piece(piece, dbcur):
    '''Execute print of JE piece'''

    #change boolean sign to Dr or Cr
    if piece[2]:
        sign = 'Dr'
    else:
        sign = 'Cr'

    #get account description
    dbcur.execute("SELECT description FROM chartofaccounts WHERE num=?", (piece[0],))
    acct_description = dbcur.fetchone()[0]

    print(sign +" "+piece[0]+" "+acct_description+" "+str(piece[1]))

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
