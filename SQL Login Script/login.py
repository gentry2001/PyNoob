##import required libraries
import sqlite3 as sql, os, re, time


##called to check if the required directory structure exists or not
##and if not create it
def dirCheck():
    
    exDir=False
    
    for count in os.listdir():
        if count == 'sql':
            exDir=True
    if exDir == False:
        os.mkdir('sql')


    
dirCheck()


cnct=sql.connect('./sql/usrAcc.db')
c=cnct.cursor()

##called to check if table exists and if not create one
def newTable():
    c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)')

    
newTable()

##assigning variables required later
f=False
t=True
valid=f
taken=f

##Text for friendly UI
fancy=["""
 ================
| SQL LOGIN TEST |
 ================
 ""","""
 ==========
| REGISTER |
 ==========
 ""","""
 =======
| LOGIN |
 =======
 ""","""
 ================
| ENTER USERNAME |
 ================
 ""","""
 ================
| ENTER PASSWORD |
 ================
"""]

fancyValid=['Please insure your password meets the following criteria:\n','8 characters length or more','1 digit or more','1 symbol or more','1 uppercase letter or more','1 lowercase letter or more',"""
Please insure your password meets the following criteria:
    8 characters length or more
    1 digit or more
    1 symbol or more
    1 uppercase letter or more
    1 lowercase letter or more
"""]



##called when a new users creds must be written to the database    
def credsWrite(username, password):
    c.execute('INSERT INTO users(username, password) VALUES (?, ?)',
              (username, password))
    cnct.commit()
    all_users=c.execute('SELECT * FROM users')
    for row in all_users.fetchall():
        print(row)
    print('Please Log In...\n')
    input('Press Enter to continue')
    userStatus=login()

##called when a new user needs to register
def userReg():
    global valid, taken
    
    print(fancy[1])
    while not valid:
        taken=False
        print(fancy[3])
        username=str(input('>>  '))
        username=str(username.upper())
        all_users = c.execute('SELECT * FROM users')
        for row in all_users.fetchall():
            if str(username) == str(row[0]):
                print('Sorry, but that username has already been taken...\nPlease enter another\n>  ')
                taken=True
        if not taken:
            print(fancy[4])
            validPass=False
            while not validPass:
                


                password=str(input('\n>>  '))

                # calculating the length
                length_error = len(password) < 8

                # searching for digits
                digit_error = re.search(r"\d", password) is None

                # searching for symbols
                symbol_error = re.search(r"[ \W _]", password) is None
                
                # searching for uppercase
                uppercase_error = re.search(r"[A-Z]", password) is None

                # searching for lowercase
                lowercase_error = re.search(r"[a-z]", password) is None


                # overall result
                errors=[length_error,digit_error,symbol_error,uppercase_error,lowercase_error]
                n=0
                toDo=[fancyValid[0]]
                e=0
                for count in errors:
                    n=n+1
                    if count == True:
                        e=e+1
                        toDo.append((fancyValid[(n)]))
                if e > 0:
                    for count in toDo:
                        print(count)
                validPass = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )


            credsWrite(username, password)
            valid=True
        
##called when an existing user need to log in
def login(n=0, timeout=2.5):
    while True:
        print(fancy[3])
        usernm=input('\n>>  ')  
        usernm=str(usernm.upper())
        print(fancy[4])
        passwd=str(input('\n>>  '))
        dbacc=c.execute('SELECT * FROM users WHERE username=? AND password=?', (usernm,passwd,))
        match=dbacc.fetchall()
        if match:
            print('Logged In!')
            return True
            break
        elif not match:
            n=n+1
            if n < 4:
                print('\n\nINVAILD CREDIDENTIALS..\nPlease Try Again')
            if n == 4:
                n=3
                if timeout < 300:
                    timeout=timeout * 2
                    print('\n\nINVAILD CREDIDENTIALS..\nPlease Try Again in (',timeout,') seconds')
                    time.sleep(timeout)
        

##MAIN MENU - Called to take users first option
def startUp():
    print(fancy[0])
    chosen=False
    while not chosen:
        try:
            opt=int(input('\n Please choose one of the options below:\n\n-> Register for a new account [1]\n-> Login to an existing account [2]\n\nPlease type a number...\n\n>>  '))
        except:
            print('\n\nPLEASE TYPE EITHER 1 OR 2...\n ')
            badInput=True
        if not badInput:
            if opt==1:
                creds=userReg()
                chosen=True
            elif opt==2:
                userStatus=login()
                chosen=True
            else:
                print('\n\nPLEASE TYPE EITHER 1 OR 2...\n ')

##start the program
if __name__ == "__main__":
    startUp()
