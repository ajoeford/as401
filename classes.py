#
#Classes
#

from decimal import *
import sqlite3
import utility

class DatabaseManager(object):
    '''Class to handle sqlite3 connection'''

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def query(self, *args):
        self.cur.execute(*args)
        self.conn.commit()
        return self.cur

    def fetchone(self):
        return self.cur.fetchone()

    def fetchall(self):
        return self.cur.fetchall()

    def __del__(self):
        self.conn.close()

class DBManagerDatetime(DatabaseManager):
    """Class to handle sqlite3 connection with datetime parsing"""

    def __init__(self, db):

        sqlite3.register_adapter(Decimal, self.adapt_decimal)
        sqlite3.register_converter("decimal", self.convert_decimal)

        self.conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cur = self.conn.cursor()

    def adapt_decimal(self, dec_in):
        return str(dec_in)

    def convert_decimal(self, dec_out):
        return Decimal(dec_out)

class TBAccount(object):
    """Class for individual TB Accounts
    String acct_num = account number
    String acct_name =  account name"""

    def __init__(self, acct_num, acct_name, acct_classification):
        super(TBAccount, self).__init__()
        self.acct_num = acct_num
        self.acct_name = acct_name
        self.acct_classification = acct_classification

    def get_acct_num(self):
        return self.acct_num

    def get_acct_name(self):
        return self.acct_name

    def get_acct_classification(self):
        return self.acct_classification

    def set_acct_name(self, new_name):
        self.acct_name = new_name

    def set_acct_classification(self, new_classification):
        self.acct_classification = new_classification


class JournalPiece(object):
    """Class for a debit or credit in a J/E
    TBAccount acct = account object
    Decimal value = entry value
    Boolean debit = true if debit, false if credit"""

    def __init__(self, acct, value, debit, je_num):
        super(JournalPiece, self).__init__()
        self.acct = acct
        self.value = value #crashes if input is not a number
        self.debit = debit
        self.je_num = je_num

    def get_acct(self):
        return self.acct

    def get_value(self):
        return self.value

    def is_debit(self):
        return self.debit

    def get_je_num(self):
        return self.je_num

    def print_line(self, dbcon):
        #Return line with account description pulled from DB
        self.acct_description = utility.get_acct_description(self.acct, dbcon)

        if self.debit == True:
            return "Dr " + self.acct +" "+ self.acct_description+" " + str(self.value)
        else:
            return "Cr " + self.acct +" "+ self.acct_description+" " + str(self.value)

    def __repr__(self):

        value_str = str(self.value)

        if self.debit == True:
            return "Dr " + self.acct + " " + str(self.value)
        else:
            return "Cr " + self.acct + " " + str(self.value)

class JournalEntry(object):
    """Class for full J/E
    Integer number = journal entry number
    String description = journale entry description
    JournalPiece[] pieces = arraylist of debit/credit pieces"""

    def __init__(self, number, description, pieces):
        super(JournalEntry, self).__init__()
        self.number = number
        self.description = description
        self.pieces = pieces

    def get_number(self):
        return self.number

    def get_description(self):
        return self.description

    def get_pieces(self):
        return self.pieces

    def is_balanced(self):
        '''Test to see if debits = credits'''
        self.debits = Decimal(0)
        self.credits = Decimal(0)
        for piece in self.pieces:
            if piece.is_debit():
                self.debits += piece.get_value()
            else:
                self.credits += piece.get_value()

        return self.debits == self.credits

    def __str__(self):
        out = str(self.number)
