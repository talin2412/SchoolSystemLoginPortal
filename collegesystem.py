import mysql.connector as mysql

db = mysql.connect(host='localhost',user='root',password='',database='college')
command_handler = db.cursor(buffered=True)

def teacher_portal():
    while 1:
        print('teacher portal')
        print('1. mark student register')
        print('2. view register')
        print('5. Logout')

        user_option = input(str("option: "))
        if user_option == '1':
            print('\nMark student Register')
            command_handler.execute('SELECT username FROM users WHERE priviledge = "student"')
            records = command_handler.fetchall()
            date = input(str('date: DD/MM/YYYY : '))
            for record in records:
                record = str(record).replace("'","")
                record = str(record).replace(",","")
                record = str(record).replace("(","")
                record = str(record).replace(")","")
                status = input(str('status for ' + str(record) + 'P/A/L'))
                query_vals = (str(record),date,status)
                command_handler.execute('INSERT INTO attendance (username, date, status) VALUES(%s,%s,%s)', query_vals)
                db.commit()
                print(record + 'Marked as ' + status)
        elif user_option == '2':
            print('\nviewing student register')
            command_handler.execute("SELECT username, date, status FROM attendance")
            records = command_handler.fetchall()
            for record in records:
                print(record)
        elif user_option == '3':
            break
        else:
            print('no valid option')

def student_portal(username):
    while True:
        print('\n1.View Register')
        print('2.Logout')

        user_option = input(str('option: '))
        if user_option == '1':
            username = (str(username),)
            command_handler.execute('SELECT date, username, status FROM attendance WHERE username = %s', username)
            records = command_handler.fetchall()
            for record in records:
                print(record)
        elif user_option == '2':
            break
        else:
            print('not a valid option')


def auth_student():
    print('\nStudent login\n')
    username = input(str('username: '))
    password = input(str('password: '))
    query_vals = (username, password, "student")
    command_handler.execute("SELECT username FROM users WHERE username = %s AND password = %s AND priviledge = %s", query_vals)
    if command_handler.rowcount <= 0:
        print('invalid login')
    else:
        student_portal(username)



def auth_teacher():
    print('\n Teacher Login\n')
    username = input(str('username: '))
    password = input(str('password: '))
    query_vals = (username, password)
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND priviledge = 'teacher'", query_vals)
    if command_handler.rowcount <= 0:
        print('not a valid login')
    else:
        teacher_portal()

def admin_session():
    while 1:
        print('\nadmin menu')
        print('1. Register a new student')
        print('2. Register a new teacher')
        print('3. Delete existing student')
        print('4. Delete existing teacher')
        print('5. Logout')

        user_option = input(str('Option: '))
        if user_option == '1':
            print('\nRegister new student')
            username = input(str('Student username : '))
            password = input(str('Student Password : '))
            query_vals = (username, password)
            command_handler.execute("INSERT INTO users (username,password,priviledge) VALUES (%s,%s,'student')", query_vals)
            db.commit()
            print('\n' + username + " has been registered")
        elif user_option == '2':
            print('\nRegister new teacher')
            username = input(str('Teacher username : '))
            password = input(str('Teacher Password : '))
            query_vals = (username, password)
            command_handler.execute("INSERT INTO users (username,password,priviledge) VALUES (%s,%s,'teacher')", query_vals)
            db.commit()
            print('\n' + username + " has been registered")
        elif user_option == '3':
            print("\nDelete existing student account")
            username = input(str("student username: "))
            query_vals = (username, 'student')
            command_handler.execute("DELETE FROM users WHERE username = %s AND priviledge = %s ", query_vals)
            db.commit()
            if command_handler.rowcount > 1:
                print('The account' + username + 'has been terminated')
            else:
                print('There is no account associated with ' + username)
        elif user_option == '4':
            print("\nDelete existing teacher account")
            username = input(str("teacher username: "))
            query_vals = (username, 'teacher')
            command_handler.execute("DELETE FROM users WHERE username = %s AND priviledge = %s ", query_vals)
            db.commit()
            if command_handler.rowcount > 1:
                print('The account' + username + 'has been terminated')
            else:
                print('There is no account associated with ' + username)
        elif user_option == '5':
            break
        else:
            print('not valid')

def auth_admin():
    print('\n')
    print('admin login\n')
    username = input(str('username : '))
    password = input(str('password : '))
    if username == 'admin':
        if password == 'test':
            admin_session()
        else:
            print('Incorrect')
    else:
        print('The username is not in the system')


def main():
    while 1:
        print("Welcome to the Directory\n")
        print("1. Login as student")
        print('2. Login as teacher')
        print("3. Login as admin")

        user_option = input(str('Select Option : '))
        if user_option == '1':
            auth_student()
        elif user_option == '2':
            auth_teacher()
        elif user_option == '3':
            auth_admin()
        else:
            print('Please select a valid option')

main()