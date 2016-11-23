#Accounting application

print ""
print "wlecome to AS401"
print "the premier accounting softwre for businesses."

running = True

#global variables
chart_of_accounts = []
gl = []

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

    def __init__(self, acct, value, debit):
        super(JournalPiece, self).__init__()
        self.acct = acct
        self.value = value
        self.debit = debit

    def get_acct(self):
        return self.acct

    def get_value(self):
        return self.value

    def is_debit(self):
        return self.debit

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
        debits = 0
        credits = 0
        for piece in self.pieces:
            if piece.is_debit:
                debits += piece.get_value
            else:
                credits += piece.get_value
        return debits == credits

    def __str__(self):
        out = str(self.number)


def aje_module():
    aje_running = True

    while aje_running:
        print ""
        print "lOL ajes"
        print ""

        user_input = raw_input("Enter Command: ")

        if user_input == "X":
            aje_running = False

def create_account():
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

def delete_account():
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
            chart_of_accounts.remove(to_delete)

def Chart_module():
    global chart_of_accounts
    chart_running = True

    while chart_running:
        print ""
        print "TB Accounts Module"
        print ""

        print "1) Create New Account"
        print "2) Edit Existing Account"
        print "3) View Chart of Accounts"
        print "4) Delete Existing Account"
        print "X) Exit\n"

        user_input = raw_input("Enter Command: ")

        if user_input == "X":
            chart_running = False

        elif user_input == "1":
            create_account()

        elif user_input == "2":
            edit_account()

        elif user_input == "3":
            print ""

            if not chart_of_accounts:
                print("No TB Accounts.")

            for account in chart_of_accounts:
                print account.get_acct_num() + ' ' + account.get_acct_name()

        elif user_input == "4":
            delete_account()

def Main():
    global running
    print "1) Enter J/E"
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
        Chart_module()

while running:

    Main()
