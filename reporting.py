#
#Reporting Module
#
import ajemodule
import pickle
from classes import *
from utility import *
import datetime

def get_account_gl(acct_num, dbcon):
    """
    Takes TB account number and returns that account's GL detail
    Parameters: String acct_num
    returns: list of GL lines
    """
    db = DBManagerDatetime(dbcon)

    db.query("SELECT * FROM gl WHERE account=?",(acct_num,))
    gl_pieces = db.fetchall()

    return gl_pieces

def get_account_balance(acct_num, dbcon):
    """
    Summary: Takes TB account number, returns TB account balance
    Parameters: String acct_num
    returns: Decimal balance
    """
    db = DBManagerDatetime(dbcon)

    db.query("SELECT * FROM gl WHERE account=?",(acct_num,))
    je_pieces = db.fetchall()

    total = Decimal(0)
    for piece in je_pieces:
        #tests debit/credit and makes credits negative for total
        if not piece[3]:
            total -= piece[2]
        else:
            total += piece[2]

    return total

def get_account_balance_dated(asof_date, acct_num, dbcon):
    """
    Takes date and acct number and returns account balance at that date.
    Parameters: Datetime.date asof_date, String acct_num
    returns: Decimal balance
    """
    db = DBManagerDatetime(dbcon)

    #add a day to asof_date and then convert to Datetime
    #this allows sql comparison of datetimes
    asof_date += datetime.timedelta(days=1)
    asof_datetime = datetime.datetime(asof_date.year, asof_date.month, asof_date.day)

    db.query("SELECT * FROM gl WHERE account =? AND entry_date <?",(acct_num, asof_datetime))
    je_pieces = db.fetchall()

    total = Decimal(0)
    for piece in je_pieces:
        #tests debit/credit and makes credits negative for total
        if not piece[3]:
            total -= piece[2]
        else:
            total += piece[2]

    return total

def view_account_gl_prompt(dbcon):
    """
    Asks for account, prints GL detail of account
    """
    account_query = int(raw_input("Enter Account #: "))

    if account_exists(account_query, dbcon):
        gl_lines = get_account_gl(account_query, dbcon)

        for line in gl_lines:
            print(ajemodule.print_piece(line, dbcon))

    else:
        print("TB account not found.")

def view_balance_prompt(dbcon):
    """
    Prints TB account, description, and balance
    """

    account_query = int(raw_input("Enter Account #: "))

    if account_exists(account_query, dbcon):
        #get account description
        acct_description = get_acct_description(account_query,dbcon)

        #get account total
        acct_balance = get_account_balance(account_query,dbcon)

        print(str(account_query)+" "+acct_description+" "+decify(acct_balance))

    else:
        print("TB account not found.")

def view_balance_date_prompt(dbcon):
    """
    Function to print TB Account#, description, and balance as of a date
    """

    account_query = int(raw_input("Enter Account #: "))

    if account_exists(account_query, dbcon):

        date_query = raw_input("Enter date (MM/DD/YYYY): ")

        #convert user input to datetime.date
        try:
            date_formatted = convert_string_date(date_query)
        except ValueError:
            print("Improper date format.")
            return null

        #get account description
        acct_description = get_acct_description(account_query,dbcon)

        #get account total
        acct_balance = get_account_balance_dated(date_formatted,account_query,dbcon)

        print(str(account_query)+" "+acct_description+" "+decify(acct_balance))

    else:
        print("TB account not found.")


def reporting_module(dbcon):
    running = True

    while running:
        print ""
        print "1) View Account Balance"
        print "2) View Account Balance at Date"
        print "3) View Account Detail"
        print "6) View TB"
        print "X) Back\n"

        user_input = raw_input("Enter Command: ")

        if user_input == "X" or user_input == "x":
            running = False

        elif user_input == "1":
            view_balance_prompt(dbcon)

        elif user_input == "2":
            view_balance_date_prompt(dbcon)

        elif user_input == "3":
            view_account_gl_prompt(dbcon)

        elif user_input == "8":
            pass
