#Name: Marquis Lewis
#Project Number: 2

from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector

db = mysql.connector.connect(
    user='root',
    password='Homelikelight96?',
    host='localhost',
    database='company',
    auth_plugin='mysql_native_password'
)
dbCursor = db.cursor(buffered=True)

if __name__ == "__main__":
    choice = -1
    #Provides menu until person quits
    while choice != 0:
        print("Main Menu")
        print("0 - Quit")
        print("1 - Add New Employee")
        print("2 - View Employee Record")
        print("3 - Add Dependent")
        print("4 - View Dependent")
        print("5 - Modify Employee Record")
        print("6 - Remove Dependent")
        print("7 - Remove employee")
        choice = int(input("Enter your choice: "))
        #makes sure people only pick options that are provided
        if choice < 0 or choice > 7:
            print("Sorry this is an invalid choice please try again")
        elif choice == 0:
            print("Thanks for using my database")
        else:
            #Add new Employee
            if choice == 1:
                #get values
                Fname = input("What is the First Name?")
                Minit = input("what is the middle initial?")
                Lname = input("what is the Last Name?")
                Ssn = str(input("what is the Ssn?"))
                Bday = int(input("what day of the month was the employee born?"))
                Bmonth = int(input("what month was the employee born?"))
                Byear = int(input("what year was the employee born?"))
                Bdate = date(Byear, Bday, Bmonth)
                Address = input("what is the Address? (number street, city, state)")
                sex = input("what is the sex? (M or F)")
                salary = "{:.2f}".format(int(input("What is the salary of the employee?")))
                Super_ssn = input("what is the supervisors ssn?")
                Dno = int(input("what is the department number?"))
                #do sql command
                add_employee = ("INSERT INTO employee "
                               "(Fname, Minit, Lname, Ssn, Bdate, Address, Sex, Salary, Super_ssn, Dno) "
                               "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                data = (Fname, Minit, Lname, Ssn, Bdate, Address, sex,salary, Super_ssn, Dno)
                dbCursor.execute(add_employee, data)
                db.commit()
                print("\n New Employee Added")

            #view employee record
            elif choice == 2:
                #get ssn
                emp_ssn = int(input("Enter the SSN of the employee: "))
                getStatement = "Select * from employee where Ssn = %s"
                dbCursor.execute(getStatement, (emp_ssn,))
                x = 0
                for i in dbCursor:
                    x = i[0]
                #check to see if provided ssn is there
                if x == 0:
                    print("I am sorry this employee:" + str(emp_ssn) + " doesn't exist")
                else:
                    #preform sql statement
                    print("\n")
                    select_stmt = "SELECT * FROM employee where Ssn = %s"
                    dbCursor.execute(select_stmt, (emp_ssn,))
                    for x in dbCursor:
                        print("Fname:", x[0])
                        print("Minit:", x[1])
                        print("Lname:", x[2])
                        print("Ssn:", x[3])
                        print("Bdate:", x[4])
                        print("Address:", x[5])
                        print("Sex:", x[6])
                        print("Salary:", x[7])
                        print("Super_ssn:", x[8])
                        print("Dno:", x[9])

                    #get manager name
                    select_stmt = "SELECT s.Fname FROM employee e, employee s where s.ssn = e.Super_ssn and e.ssn = %s"
                    dbCursor.execute(select_stmt, (emp_ssn,))
                    for x in dbCursor:
                        print("Manager Name:", x[0])

                    #get department name
                    select_stmt = "SELECT Dname FROM department, Employee where Dno = Dnumber and Ssn = %s"
                    dbCursor.execute(select_stmt, (emp_ssn,))
                    for x in dbCursor:
                        print("Department Name:", x[0])

            #add dependent
            elif choice == 3:
                #get ssn
                Essn = input("What is the Employees ssn?")
                select_stmt = "SELECT * FROM dependent where Essn = %s"
                dbCursor.execute(select_stmt, (Essn,))
                lock = []
                for i in dbCursor:
                    x = i[0]
                #checks to see if ssn is real
                if x == 0:
                    print("I am sorry this employee:" + str(emp_ssn) + " doesn't exist")
                else:
                    #gives list of dependets if they have any
                    for x in dbCursor:
                        lock.insert(0, True)
                        print("Essn:", x[0])
                        print("Dependent Name:", x[1])
                        print("Sex:", x[2])
                        print("Bdate", x[3])
                        print("Relationship:", x[4])
                    if len(lock) >= 1:
                        print("These are the dependents the employee already has")
                    else:
                        print("")
                    #gets values to add dependent
                    Dependent_name = input("What is the dependents name?")
                    Sex = input("what is the sex? (M or F)")
                    Byear = int(input("what is the Birth year?"))
                    Bmonth = int(input("what is the Birth month?"))
                    Bday = int(input("what is the Birth day?"))
                    Bdate = date(Byear, Bmonth, Bday)
                    Relationship = input("what is the Relationship to Employee?")

                    #preform SQL statement
                    add_dependent = ("INSERT INTO dependent "
                                    "(Essn, Dependent_name, Sex, Bdate, Relationship)"
                                    "VALUES (%s,%s,%s,%s,%s)")
                    data = (Essn, Dependent_name, Sex, Bdate, Relationship)
                    dbCursor.execute(add_dependent, data)
                    db.commit()
                    print("\n New dependent Added")
            #View dependents
            elif choice == 4:
                #get ssn
                emp_ssn = int(input("Enter the employee ssn to see dependents: "))
                getStatement = "Select * from dependent where Essn = %s"
                dbCursor.execute(getStatement, (emp_ssn,))
                x = 0
                for i in dbCursor:
                    x = i[0]
                #checks if ssn is real
                if x == 0:
                    print("I am sorry this employee:" + str(emp_ssn) + " doesn't exist")
                else:
                    #list all names of dependents
                    select_stmt = "SELECT * FROM dependent where Essn = %s"
                    dbCursor.execute(select_stmt, (emp_ssn,))
                    for x in dbCursor:
                        print("Dependent Name:", x[1])

                    #allow user to pick dependent they would like to see
                    kid = (input("Enter the name of the dependent you would like to see: "))
                    selectStatement = "Select * from dependent where Dependent_name = %s"
                    dbCursor.execute(selectStatement, (kid,))
                    for x in dbCursor:
                        print("Dependent Name:", x[1])
                        print("Sex:", x[2])
                        print("Bdate", x[3])
                        print("Relationship:", x[4])


            #modify employee records
            elif choice == 5:
                #get SSN
                emp_ssn = int(input("Enter the ssn of employee you want to modify:"))
                getStatement = "Select * from employee where Ssn = %s for update"
                dbCursor.execute(getStatement, (emp_ssn,))
                x = 0
                for i in dbCursor:
                    x = i[0]
                #check if its real
                if x == 0:
                    print("I am sorry this employee:" + str(emp_ssn) + " doesn't exist")
                else:
                    #provide information about employee about to be eddited
                    select_stmt = "SELECT * FROM employee where Ssn = %s"
                    dbCursor.execute(select_stmt, (emp_ssn,))
                    for x in dbCursor:
                        print("Fname:", x[0])
                        print("Minit:", x[1])
                        print("Lname:", x[2])
                        print("Ssn:", x[3])
                        print("Bdate:", x[4])
                        print("Address:", x[5])
                        print("Sex:", x[6])
                        print("Salary:", x[7])
                        print("Super_ssn:", x[8])
                        print("Dno:", x[9])
                    print("This is the Employee You will be editing")

                    #asks what values they want to change
                    print("\nPlease enter Y or N for the next questions")
                    Caddress = (input("Would you like to change Address:"))
                    Csex =  (input("Would you like to change Sex:"))
                    Csalary = (input("Would you like to change Salary:"))
                    Csuper_ssn =  (input("Would you like to change Super_ssn:"))
                    CDno = (input("Would you like to change Department Number:"))

                    #goes through each value requested to be changed and preform sql statement
                    if Caddress == 'Y':
                        newAddress = (input("Whats the new address?:"))
                        updateStatement = "Update employee set Address= %s where Ssn = %s"
                        dbCursor.execute(updateStatement, (newAddress, emp_ssn,))
                        db.commit()
                    if Csex == 'Y':
                        newSex = (input("Whats the new sex?:"))
                        updateStatement = "Update employee set Sex=%s where Ssn = %s"
                        dbCursor.execute(updateStatement, (newSex, emp_ssn,))
                        db.commit()
                    if Csalary == 'Y':
                        newSalary = "{:.2f}".format(int(input("What is the new salary?:")))
                        updateStatement = "Update employee set Salary= %s where Ssn = %s"
                        dbCursor.execute(updateStatement, (newSalary, emp_ssn,))
                        db.commit()
                    if Csuper_ssn == 'Y':
                        newSuper_ssn = (input("Whats the new Super_ssn?:"))
                        updateStatement = "Update employee set Super_ssn= %s where Ssn = %s"
                        dbCursor.execute(updateStatement, (newSuper_ssn, emp_ssn,))
                        db.commit()
                    if CDno == 'Y':
                        newDno = (input("Whats the new Department Number?:"))
                        updateStatement = "Update employee set Dno= %s where Ssn = %s"
                        dbCursor.execute(updateStatement,(newDno, emp_ssn,))
                        db.commit()

                    print("Change Completed")

                    #prints new data for changed employee
                    select_stmt = "SELECT * FROM employee where Ssn = %s"
                    dbCursor.execute(select_stmt, (emp_ssn,))
                    for x in dbCursor:
                        print("Fname:", x[0])
                        print("Minit:", x[1])
                        print("Lname:", x[2])
                        print("Ssn:", x[3])
                        print("Bdate:", x[4])
                        print("Address:", x[5])
                        print("Sex:", x[6])
                        print("Salary:", x[7])
                        print("Super_ssn:", x[8])
                        print("Dno:", x[9])
            #Remove dependent
            elif choice == 6:
                #get ESSN
                emp_ssn = int(input("Enter the employee ssn to see dependents: "))
                getStatement = "Select * from dependent where Essn = %s for update"
                dbCursor.execute(getStatement, (emp_ssn,))
                x = 0
                for i in dbCursor:
                    x = i[0]
                #checks if ESSN exsists
                if x == 0:
                    print("I am sorry this employee:" + str(emp_ssn) + " doesn't exist")
                else:
                    #print all dependents employee already has
                    print("\n")
                    select_stmt = "SELECT * FROM dependent where Essn = %s"
                    dbCursor.execute(select_stmt, (emp_ssn,))
                    for x in dbCursor:
                        print("Essn:", x[0])
                        print("Dependent Name:", x[1])
                        print("Sex:", x[2])
                        print("Bdate", x[3])
                        print("Relationship:", x[4])

                #get name of depenedent to be deleted and deletes
                bye_bye = (input("Enter the name of the dependent you would like to delete: "))
                deleteStatement = "Delete from dependent where Dependent_name = %s"
                dbCursor.execute(deleteStatement, (bye_bye,))
                db.commit()

                print("Dependent Deleted")

                #prints new list of dependents
                select_stmt = "SELECT * FROM dependent where Essn = %s"
                dbCursor.execute(select_stmt, (emp_ssn,))
                for x in dbCursor:
                    print("Essn:", x[0])
                    print("Dependent Name:", x[1])
                    print("Sex:", x[2])
                    print("Bdate", x[3])
                    print("Relationship:", x[4])

            #remove employee
            elif choice == 7:
                #get ssn
                emp_ssn = int(input("Enter the ssn of the employee: "))
                getStatement = "Select * from employee where Ssn = %s"
                dbCursor.execute(getStatement, (emp_ssn,))
                x = 0
                for i in dbCursor:
                    x = i[0]
                #checks if ssn is real
                if x == 0:
                    print("I am sorry this employee: " + str(emp_ssn) + " doesn't exist")
                else:
                    #prints out current information about employee
                    print("\n")
                    select_stmt = "SELECT * FROM employee where Ssn = %s"
                    dbCursor.execute(select_stmt, (emp_ssn,))
                    for x in dbCursor:
                        print("Fname:", x[0])
                        print("Minit:", x[1])
                        print("Lname:", x[2])
                        print("Ssn:", x[3])
                        print("Bdate:", x[4])
                        print("Address:", x[5])
                        print("Sex:", x[6])
                        print("Salary:", x[7])
                        print("Super_ssn:", x[8])
                        print("Dno:", x[9])

                    #confirms deletion
                    print("Please reply to next question with Y or N")
                    confirm = input("Are you sure you want to delete this employee?: ")
                    if confirm == 'Y':
                        select_stmt = "SELECT * FROM dependent where Essn = %s"
                        dbCursor.execute(select_stmt, (emp_ssn,))
                        lock = []
                        #if there are dpeendents, prints them
                        for x in dbCursor:
                            lock.insert(0, True)
                            print("Essn:", x[0])
                            print("Dependent Name:", x[1])
                            print("Sex:", x[2])
                            print("Bdate", x[3])
                            print("Relationship:", x[4])
                        #if there are dpeendents dont delete
                        if len(lock) >= 1:
                            print("This employee still has dependents in the system, please delete dependents first")
                        #if no dependents delete
                        else:
                            deleteStatement = "Delete from employee where Ssn = %s"
                            dbCursor.execute(deleteStatement, (emp_ssn,))
                            db.commit()
                            print("Employee Deleted")

