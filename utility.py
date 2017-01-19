import classes
from decimal import Decimal
import datetime

def account_exists(acct_num, dbcon):
    """Test to see if account exists
        returns boolean"""
    db = classes.DBManagerDatetime(dbcon)

    db.query("SELECT * FROM chartofaccounts WHERE num=?", (acct_num,))
    if db.fetchone():
        return True
    else:
        return False

def decify(num):
    '''
    Takes Decimal, adds commas and decimal point and returns as String
    Parameter: Decimal num
    returns String'''

    as_str = str(num)
    outs = as_str[:]

    if "." not in as_str:
        outs = outs + ".00"

    #add commas
    if num > 999 or num < -999:
        outs = outs[0:-6]+','+outs[-6:]
    if num > 999999 or num < -999999:
        outs = outs[0:-10]+','+outs[-10:]
    if num > 999999999 or num < -999999999:
        outs = outs[0:-14]+','+outs[-14:]
    if num > 999999999999 or num < -999999999999:
        outs = outs[0:-18]+','+outs[-18:]

    return outs

def get_acct_description(acct_num, dbcon):
    """
    get account description
    Parameters: String acct_num, String dbcon
    returns: String account description of first account found in db
    """

    db = classes.DBManagerDatetime(dbcon)

    db.query("SELECT description FROM chartofaccounts WHERE num=?", (acct_num,))
    return db.fetchone()[0]

def convert_string_date(string_date):
    """
    Parameters: String string_date as (MM/DD/YYYY)
    returns: Datetime date
    """

    month = int(string_date[0:2])
    day = int(string_date[3:5])
    year = int(string_date[-4:])

    date_formatted = datetime.date(year, month, day)

    return date_formatted
