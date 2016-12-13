#
#Reporting Module
#
from decimal import *
import pickle
from classes import *

def get_acct_description(acct_num, dbcur):
    #get account description
    dbcur.execute("SELECT description FROM chartofaccounts WHERE num=?", (acct_num,))
    return dbcur.fetchone()[0]

def je_piece_loop(aje_lines_list, aje_lines, input_sign, input_acct, input_value, dbcur):
    """Loop for JE lines"""
    """parameters:
    List aje_lines_list
    Int aje_lines
    String input_sign
    String input_acct
    Decimal input_value

    returns: A tuple of updated aje_lines_list and aje_lines
    """

    looped = True
    while looped:
        print("")
        for line in aje_lines_list:
            print("* " + line.print_line(dbcur))
        print(str(aje_lines) + " " + input_sign + " " + input_acct +
            " "+ get_acct_description(input_acct,dbcur) +" " + input_value)

        input_confirm = raw_input("Is this line correct?(Y/N): ")

        if input_confirm == 'Y' or input_confirm == 'y':

            #prep debit/credit sign
            if input_sign == 'Dr':
                input_debit = True
            else:
                input_debit = False

            #create JE piece and add to list
            try:
                journal_piece = JournalPiece(input_acct, input_value, input_debit, aje_count)
                aje_lines_list.append(journal_piece)
                aje_lines += 1
            except:
                print("Error processing JE line. Line not entered.")

            return (aje_lines_list, aje_lines)

        elif input_confirm == 'N' or input_confirm == 'n':
            return (aje_lines_list, aje_lines)

def confirm_je_loop(aje_count, input_description, aje_lines_list, dbcon):
    """
    parameters:
    Int aje_count
    String input_description
    JournalPiece[] aje_lines_list

    returns: Tuple of updated aje_count and aje_lines_loop.

    If not canceled, adds JE to je_list and gl lists
    """
    global je_list
    global gl
    aje_lines_loop = True

    dbcur = dbcon.cursor()

    final_loop = True
    while final_loop:
        input_final = raw_input("Is this journal entry complete?(Y/N/eXit) ")

        if input_final == 'Y' or input_final == 'y':
            new_je = JournalEntry(aje_count, input_description, aje_lines_list)
            if new_je.is_balanced():
                for entry in new_je.get_pieces():
                    dbcur.execute("INSERT INTO gl VALUES (?,?,?,?,?)",
                    (entry.get_acct(), entry.get_value(), entry.is_debit(), aje_count, input_description))
                    dbcon.commit()

                print "JE entered."
                aje_count += 1
                final_loop = False
                aje_lines_loop = False

            else:
                print "JE not in balance."

                for entry in new_je.get_pieces():
                    print "*" + str(entry)
                final_loop = False

        elif input_final == 'N' or input_final == 'n':
            final_loop = False

        elif input_final == 'X' or input_final == 'x':
            final_loop = False
            aje_lines_loop = False

    return (aje_count, aje_lines_loop)

def account_exists(acct_num, dbcur):
    """Test to see if account already exists
        returns boolean"""

    dbcur.execute("SELECT * FROM chartofaccounts WHERE num=?", (acct_num,))
    if dbcur.fetchone():
        return True
    else:
        return False

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

def view_je(dbcon):
    """
    Prints JE's based on JE number
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
