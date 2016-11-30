#Accounting application

from decimal import *
import sqlite3
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
    Integer value = entry value
    Boolean debit = true if debit, false if credit"""

    def __init__(self, acct, value, debit, je_num):
        super(JournalPiece, self).__init__()
        self.acct = acct
        self.value = Decimal(value)
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

    def __repr__(self):
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

def je_line_loop(aje_lines_list, aje_lines, input_sign, input_acct, input_value):
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
        for line in aje_lines_list:
            print "* " + str(line)
        print(str(aje_lines) + " " + input_sign + " " + input_acct + " " + input_value)
        print ""
        input_confirm = raw_input("Is this line correct?(Y/N): ")

        if input_confirm == 'Y' or input_confirm == 'y':

            #prep debit/credit sign
            if input_sign == 'Dr':
                input_debit = True
            else:
                input_debit = False

            #create JE piece and add to list
            journal_piece = JournalPiece(input_acct, input_value, input_debit, aje_count)
            aje_lines_list.append(journal_piece)
            aje_lines += 1

            return (aje_lines_list, aje_lines)

        elif input_confirm == 'N' or input_confirm == 'n':
            return (aje_lines_list, aje_lines)

def confirm_je_loop(aje_count, input_description, aje_lines_list):
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

    final_loop = True
    while final_loop:
        input_final = raw_input("Is this journal entry complete?(Y/N/eXit) ")
        print ""

        if input_final == 'Y' or input_final == 'y':
            new_je = JournalEntry(aje_count, input_description, aje_lines_list)
            if new_je.is_balanced():
                for entry in new_je.get_pieces():
                    gl.append(entry)
                je_list.append(new_je)
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

def create_aje():
    """Make an AJE"""
    global gl
    global aje_count
    global je_list

    aje_lines_list = []

    print ""
    print "Journal Entry #" + str(aje_count)
    input_description = raw_input("Enter J/E description: ")

    aje_lines = 1
    aje_lines_loop = True
    while aje_lines_loop:
        print ""
        print "JE Line " + str(aje_lines) + ":"

        input_acct = raw_input("Enter account: ")
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
        updated_ajes = je_line_loop(aje_lines_list, aje_lines, input_sign, input_acct, input_value)
        aje_lines_list = updated_ajes[0]
        aje_lines = updated_ajes[1]

        #confirmation of full JE
        updated_confirm_loop = confirm_je_loop(aje_count, input_description, aje_lines_list)
        aje_count = updated_confirm_loop[0]
        aje_lines_loop = updated_confirm_loop[1]

def print_je(je):
    print(str(je.get_number()) + str(je.get_description()))
    for je_line in je.get_pieces():
        print(je_line)

def view_je():
    """
    Prints JE's based on JE number
    """

    je_query = int(raw_input("Lookup JE by #: "))

    for je in je_list:
        if je_query == je.get_number():
            print_je(je)
            print("")
            break
    else:
        print("JE# not found.")

def aje_module():
    aje_running = True

    while aje_running:
        print "1) Enter J/E"
        print "2) View J/E"
        print "X) Exit\n"

        user_input = raw_input("Enter Command: ")

        if user_input == "X" or user_input == "x":
            aje_running = False

        elif user_input == "1":
            create_aje()

        elif user_input == "2":
            view_je()


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

        print acct_num + ' ' + acct_name
        print "Account Classification: " + acct_classification

        unaccepted = True
        while unaccepted:
            continue_prompt = raw_input("Is this correct? (Y/N) ")

            if continue_prompt == 'Y' or continue_prompt == 'y':
                new_account_tuple = (acct_num, acct_name, acct_classification)
                dbcur.execute("INSERT INTO chartofaccounts VALUES (?,?,?)", new_account_tuple)
                dbcon.commit()

                #Non db code:
                new_account = TBAccount(acct_num, acct_name, acct_classification)
                chart_of_accounts.append(new_account)

                unaccepted = False
                create_account_running = False

            if continue_prompt == 'N':
                unaccepted = False

def edit_account():
    """Change account name or classification based on account number"""
    global chart_of_accounts
    valid_account = ""

    acct_input = raw_input("Enter account number: ")
    for account in chart_of_accounts:
        if account.get_acct_num() == acct_input:
            valid_account = account
            break

    if valid_account != "":
        print(valid_account.get_acct_num() + " "+ valid_account.get_acct_name())
        print("Classification: " + valid_account.get_acct_classification())

        edited = False
        while edited == False:
            ask_name = raw_input("Edit account name? (Y/N) ")

            if ask_name == 'Y' or ask_name == 'y':
                new_name = raw_input("Enter new name: ")

                valid_account.set_acct_name(new_name)
                edited = True

            ask_class = raw_input("Change account classification? (Y/N) ")

            if ask_class == 'Y' or ask_class == 'y':

                acct_classification = ""
                while acct_classification not in ["A", "L", "OE", "R", "E"]:

                    print "Enter account classification (A/L/OE/R/E)"
                    acct_classification = raw_input("Classification: ")

                valid_account.set_acct_classification(acct_classification)
                edited = True

            print(valid_account.get_acct_num() + " "+ valid_account.get_acct_name())
            print("Classification: " + valid_account.get_acct_classification())
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

    for account in chart_of_accounts:
        if account.get_acct_num() == delete_num:
            to_delete = account

    if to_delete == "":
        print("Invalid account number.")

    else:
        print("Are you sure you want to delete the following account?")
        print(to_delete.get_acct_num() + " "+ to_delete.get_acct_name())
        affirm = raw_input("Delete? (Y/N) ")
        if affirm == 'Y' or affirm == 'y':
            dbcur.execute("DELETE FROM chartofaccounts WHERE num=?", (to_delete,))
            dbcon.commit()
            #old non-db code:
            chart_of_accounts.remove(to_delete)

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
        print "X) Exit\n"

        user_input = raw_input("Enter Command: ")

        if user_input == "X":
            chart_running = False

        elif user_input == "1":
            create_account(dbcur, dbcon)

        elif user_input == "2":
            edit_account()

        elif user_input == "3":
            print ""

            dbcur.execute("SELECT * FROM chartofaccounts")
            all_chart = dbcur.fetchall()

            for acct in all_chart:
                print(acct[0]+" "+acct[1])
            '''
            if not chart_of_accounts:
                print("No TB Accounts.")

            for account in chart_of_accounts:
                print account.get_acct_num() + ' ' + account.get_acct_name()
            '''
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

    elif user_input == '1':
        aje_module()
    elif user_input == '3':
        chart_module(dbcon)

while running:

    Main(dbcon)
    dbcon.close()
