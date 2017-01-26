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

def get_account_gl_dated(acct_num, date_b, date_e, dbcon):
    """
    Takes TB account number, begin date, end date; returns gl for that period
    Parameters: String acct_num, Datetime.date date_b, Datetime.date date_e
    returns: list of GL lines
    """
    db = DBManagerDatetime(dbcon)

    #add a day to end date and then convert to Datetime
    #this allows proper sql comparison of datetimes
    date_e += datetime.timedelta(days=1)
    datetime_e = datetime.datetime(date_e.year, date_e.month, date_e.day)
    #convert begin date to datetime
    datetime_b = datetime.datetime(date_b.year, date_b.month, date_b.day)

    db.query("SELECT * FROM gl WHERE account=? AND entry_date>=? AND entry_date<?"
        ,(acct_num, datetime_b, datetime_e))

    return db.fetchall()

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

def view_gl_by_date_prompt(dbcon):
    """
    Asks for account, date range, prints GL detail of account
    """
    account_query = int(raw_input("Enter Account #: "))

    if account_exists(account_query, dbcon):

        input_begindate = raw_input("Enter start date (MM/DD/YYYY): ")
        input_enddate = raw_input("Enter end date (MM/DD/YYYY): ")

        #convert user input to datetime.date
        try:
            begindate_formatted = convert_string_date(input_begindate)
            enddate_formatted = convert_string_date(input_enddate)

            gl_lines = get_account_gl_dated(account_query,begindate_formatted,
                enddate_formatted, dbcon)

            for line in gl_lines:
                print(ajemodule.print_piece(line, dbcon))

        except ValueError:
            print("Improper date format.")

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

            #get account description
            acct_description = get_acct_description(account_query,dbcon)

            #get account total
            acct_balance = get_account_balance_dated(date_formatted,account_query,dbcon)

            print(str(account_query)+" "+acct_description+" "+decify(acct_balance))

        except ValueError:
            print("Improper date format.")

    else:
        print("TB account not found.")

def get_accounts_chart(dbcon):
    """
    returns list of chart of accounts
    """

    db = DBManagerDatetime(dbcon)

    db.query("SELECT * FROM chartofaccounts ORDER BY num")
    all_chart = db.fetchall()

    return all_chart

def get_tb_dated(date_formatted, dbcon):
    """
    Compiles TB into a list
    Parameters: Datetime.date date_formatted, String dbcon
    returns: List tb_list
    """

    #get chart of accounts
    chart_of_accounts = get_accounts_chart(dbcon)

    tb_list = []
    for account in chart_of_accounts:
        #get account balance as of date
        acct_balance = get_account_balance_dated(date_formatted,account[0],dbcon)

        #add to list
        tb_list.append((account[0],account[1],acct_balance))

    return tb_list

def view_tb(dbcon):
    """
    Prompt for date and print tb
    """

    date_query = raw_input("Enter date (MM/DD/YYYY): ")

    try:
        date_formatted = convert_string_date(date_query)

        tb_list = get_tb_dated(date_formatted, dbcon)

        for account in tb_list:
            print(account[0]+" "+account[1]+" "+decify(account[2]))

    except ValueError:
        print("Improper date format.")

def reporting_module(dbcon):
    running = True

    while running:
        print ""
        print "1) View Account Balance"
        print "2) View Account Balance at Date"
        print "3) View Account Detail"
        print "4) View Account Detail (Dated)"
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

        elif user_input == "4":
            view_gl_by_date_prompt(dbcon)

        elif user_input == "6":
            view_tb(dbcon)

        elif user_input == "8":
            pass
