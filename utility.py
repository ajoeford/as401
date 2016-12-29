import classes

def decify(num):
    '''
    Takes int, divides by 100 and returns as String
    Parameter: int num
    returns String'''

    as_str = str(num)
    outs = as_str[0:-2]+'.'+as_str[-2:]

    #add commas
    if num > 99999:
        outs = outs[0:-6]+','+outs[-6:]
    if num > 99999999:
        outs = outs[0:-10]+','+outs[-10:]
    if num > 99999999999:
        outs = outs[0:-14]+','+outs[-14:]
    if num > 99999999999999:
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
