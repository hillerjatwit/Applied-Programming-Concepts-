import sqlite3
from datetime import datetime
import unittest
import os
from unittest.mock import patch
import keyboard
import time
import tkinter as tk
from tkinter import messagebox


#ClassObjects to be used




#Jared
class dbConnection:
    
    DatabaseURI="assignment5.db"
    cur=None
    db=None
    
    def __init__(self):
        self.db = sqlite3.connect(self.DatabaseURI)
        self.cur = self.db.cursor()
        
    def query(self, query):
        self.cur.execute(query)
        return self.cur.fetchone()
    
    def queryExecute(self, query):
        self.cur.execute(query)
        self.db.commit()
    
class Tests(unittest.TestCase):

    def testAddCourse(self):
        self.assertEqual('foo'.upper(), 'FOO')
    
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())
    
    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])

        with self.assertRaises(TypeError):
            s.split(2)


# if __name__ == '__main__':
#     unittest.main(verbosity=2)

## ---------------- UNIT TEST HERE  ----------------------
testactive = 0 #Regis - Only run test cases if test is set to 1
if testactive:
    with open("student_search_filter_int.txt","r") as f:#change the name of text file to change test case
        testlist = f.read().splitlines()
    #testcase=f.readlines()
    testcase = testlist[0:18] 
    login = testcase[0]
    selection = testcase[1]
    crninert = testcase[2]

    testassert = testlist[19:] #values to compare with

class User:

    #User Class Attributes
    Email=None
    Name=None
    Surname=None
    ID=None
    Type=None
    
    #SQL Database Access Objects
    conn = dbConnection()
    #Jared
    def login():
        
        #gloabl class object to hold info easily
        global stud, inst, admin, conn
        
        #Database access object
        conn = dbConnection()
        
        email = login_email_entry.get()
        password = login_password_entry.get()
          
        results = conn.query(f"SELECT ID FROM USERS WHERE EMAIL = '{email}' AND PASSWORD = '{password}'")
        if (results is not None):
            #self.Email = email
            #self.Name = self.conn.query(f"SELECT Name FROM USERS WHERE Email = '{email}' AND Password = '{password}'")
            #self.Surname = self.conn.query(f"SELECT Surname FROM USERS WHERE Email = '{email}' AND Password = '{password}'")
            ID1 = str(conn.query(f"SELECT ID FROM USERS WHERE Email = '{email}' AND Password = '{password}'"))
            ID2 = ''.join(e for e in ID1 if e.isalnum())
            ID = int(ID2)
            
            Type = conn.query(f"SELECT USERTYPE FROM USERS WHERE Email = '{email}' AND Password = '{password}'")
            if (Type[0] == 'STUDENT'):
                stud = Student(ID)
                showStudentMainpage()
            elif(Type[0] == 'INSTRUCTOR'):
                inst = Instructor(ID)
                #show instructor main page
            elif(Type[0] == 'ADMIN'):
                admin = Admin(ID)
                showAdminMainpage()
                #show admin main page
            else:
                raise TypeError("Invalid Usertype")
        else :
            raise Exception("Credentials Not Found")
            
            
    def logout(self):
        #Add GUI logic to return to login page
        
        #Set Attributes back to none
        Email=None
        Name=None
        Surname=None
        ID=None
        
    #def __init__(self, in_name):
    #    self.sur_name = in_name
    def search_all(self): #Regis
        print("Entire course table")
        query_result = self.conn.query("""SELECT * FROM COURSE""") 
        for i in query_result:
            print(i)	
        
    def search_filter(self):#Regis
        filter = int(input("\nEnter a coulumn to filter courses by\n1) CRN\n2) Title\n3) Department\n4) Time\n5) Day of the Week\n6) Semeseter\n7) Year\n8) Credits\n"))
        filterval = str(input("\nEnter the value to filter: "))
        match filter:
            case 1:
                filter = "CRN"
            case 2:
                filter = "TITLE"
            case 3:
                filter = "DEPARTMENT"
            case 4:
                filter = "TIME"
            case 5:
                filter = "DOW"
            case 6: 
                filter = "SEMESTER"
            case 7:
                filter = "YEAR"
            case 8:
                filter = "CREDITS"
            case _:
                filter = "CRN" #default to CRN if invalid input entered
                print("Invalid input entered, defaulting to CRN\n")

        print("Filtered course(s) based on " + str(filter))
        query_result = self.conn.query(f"SELECT * FROM COURSE WHERE {filter} = '{filterval}'")
        for i in query_result:
            print(i)
            if testactive:
                for count, j in enumerate(i):
                    assert str(i[count]) == str(testassert[count + 1]), f'X Results do not match. Expected Value: {testassert[count]}. Actual Value: {i[count]}'
                    print('✔ Test Passed!')       
class Student(User):
    
    conn = dbConnection()
    
    
    def __init__(self, id):
        self.ID = id

    #Jared
    def addCourse():
         #Check if CRN exists
        CRN = add_course_CRN.get()
        Add = False
        
        results = conn.query(f"SELECT * FROM COURSE WHERE CRN = '{CRN}'")
        if (results is not None):
            #Need logic to check if credits match
            row =  list(conn.query(f"SELECT CLASS1, CLASS2, CLASS3, CLASS4, CLASS5 FROM STUDENT WHERE ID = '{stud.ID}'"))
            for i in range(5):
                if row[i] is None:
                    Add = True
                    conn.queryExecute(f"UPDATE STUDENT SET CLASS{i+1} = '{CRN}' WHERE ID = '{stud.ID}'")
                    print("Class has been updated")
                    break
            if (Add):
                messagebox.showinfo(f"Course {CRN} was added")
            else:
                messagebox.showinfo(f"Course {CRN} was not added")
    #Jared
    def removeCourse():
        #Check if CRN exists
        CRN = int(remove_course_CRN.get())
        Found = False
        
        results = conn.query(f"SELECT * FROM COURSE WHERE CRN = '{CRN}'")
        if (results is not None):
            #Need logic to check if credits match
            row =  list(conn.query(f"SELECT CLASS1, CLASS2, CLASS3, CLASS4, CLASS5 FROM STUDENT WHERE ID = '{stud.ID}'"))
            for i in range(5):
                if (row[i] == CRN):
                    Found = True
                    conn.queryExecute(f"UPDATE STUDENT SET CLASS{i+1} = 'NULL' WHERE ID = '{stud.ID}'")
            
            if (Found):
                messagebox.showinfo(f"Course {CRN} was Removed")
            else:
                messagebox.showinfo(f"Course {CRN} was not Found")
            showStudentMainpage()
    
    def checkConflict(self):
        results = self.conn.query("SELECT REGISTEREDCOURSES FROM STUDENTS WHERE EMAIL = '" + self.Email+ "'")
        for row in results:
            #logic for checking for conflicts
            result =1          
            
    def printSchedule():
        #fix to print all courses
        result = conn.query(f"SELECT REGISTEREDCOURSES FROM STUDENT WHERE ID = '{stud.ID}'")
        for row in result:
            print(row)

class Instructor(User):
    #Class Attributes 
    Major=None
    LinkedCourses=None
    Title=None
    HireYear=None
    Department=None
    
    def __init__(self, in_name):
        self.roster = []    
        self.sur_name = in_name

    def print_roster(self):     #Billy Hingston
        crn = input("To see all students in the course, enter CRN of course: ")
        query_result = self.conn.query("SELECT NAME from STUDENT where CLASS1 =  '" + crn + "'")
        for i in query_result:
            app = i
            self.roster.append(app)
        query_result = self.conn.query("SELECT NAME from STUDENT where CLASS2 =  '" + crn + "'")
        for i in query_result:
            app = i
            self.roster.append(app)
        query_result = self.conn.query("SELECT NAME from STUDENT where CLASS3 =  '" + crn + "'")
        for i in query_result:
            app = i
            self.roster.append(app)
        query_result = self.conn.query("SELECT NAME from STUDENT where CLASS4 =  '" + crn + "'")
        for i in query_result:
            app = i
            self.roster.append(app)
        query_result = self.conn.query("SELECT NAME from STUDENT where CLASS5 =  '" + crn + "'")
        for i in query_result:
            app = i
            self.roster.append(app)
        namecount = 0
        for i in self.roster:
            print (i)
            if testactive:
                    assert str(i[0]) == str(testassert[namecount + 1]), f'X Results do not match. Expected Value: {testassert[count]}. Actual Value: {i[count]}'
                    print('✔ Test Passed!') 
                    namecount += 1        
    # def SearchCourseRoster(self):
    #     #IDK what this is supposed to do
    #     return True
       
class Admin(User):
    
    def __init__(self, in_name):
        self.sur_name = in_name
        
    def add_course(self):       #Micah
        addCRN = input("Enter the course CRN you want to add: ")
        results = self.conn.query(f"""Select TITLE From COURSE Where CRN = {addCRN} """)
        if (len(results)==0):
          #  testinputs = ["Hi", "CS", 10, "Thu", "Summer", 2021, 3]

            def test():
                addTitle = input("Enter the title: ")
                addDep = input("Enter the department: ")
                addTime = input("Enter the time: ")
                addDOW = input("Enter the DOW: ")
                addSem = input("Enter the semester: ")
                addYear = input("Enter the year: ")
                addCred = input("Enter the amount of credits: ")
                
                self.conn.queryExecute(f"""INSERT INTO COURSE VALUES({addCRN}, '{addTitle}','{addDep}', {addTime}, '{addDOW}', '{addSem}', {addYear}, {addCred})""") 
            # Patch the input function with a side effect to return the test inputs sequentially
            #     with patch('builtins.input', side_effect=testinputs):
                # Call the function that uses the inputs
                if testactive:
                    query_result = self.conn.query(f"""SELECT * FROM COURSE WHERE CRN = {addCRN}""") 
                    for i in query_result:
                        print(i)
                        if testactive:
                            for count, j in enumerate(i):
                                assert str(i[count]) == str(testassert[count + 1]), f'X Results do not match. Expected Value: {testassert[count]}. Actual Value: {i[count]}'
                                print('✔ Test Passed!')     
            test()  

        else:
            print("Course already has that CRN")
            
    def remove_course(self):        #Micah
        removeCRN= input("Enter the course CRN you want to remove: ")
        
        results = self.conn.query(f"""Select TITLE From COURSE Where CRN = {removeCRN} """)
        if (len(results)==0):
            print("A course with that CRN does not exist")
        else:
            self.conn.queryExecute(f"""DELETE FROM COURSE WHERE CRN = {removeCRN}""")
            
    def remove_course_student(self):            #Micah
        stuID=input("Please enter a students ID: ")
        results = self.conn.query(f"""Select CLASS1,CLASS2,CLASS3,CLASS4,CLASS5 From STUDENT Where ID = {stuID} """)
        
        for i in results:
            print("The courses being taken are:")
            print(i)
        removeclass =input("Which course do you want to remove?")
        self.conn.queryExecute(f"UPDATE STUDENT SET CLASS1 = NULL WHERE CLASS1 = {removeclass} AND ID = {stuID}")
        self.conn.queryExecute (f"UPDATE STUDENT SET CLASS2 = NULL WHERE CLASS2 = {removeclass} AND ID = {stuID}")
        self.conn.queryExecute(f"UPDATE STUDENT SET CLASS3 = NULL WHERE CLASS3 = {removeclass} AND ID = {stuID}")
        self.conn.queryExecute(f"UPDATE STUDENT SET CLASS4 = NULL WHERE CLASS4 = {removeclass} AND ID = {stuID}")
        self.conn.queryExecute(f"UPDATE STUDENT SET CLASS5 = NULL WHERE CLASS5 = {removeclass} AND ID = {stuID}")

    def add_course_student(self):               #Micah
        stuID=input("Please enter a students ID: ")
        ClassAdd=input("Enter the course CRN you want to add: ")
        cursor.execute(f"""Select CLASS1,CLASS2,CLASS3,CLASS4,CLASS5 From STUDENT Where ID = {stuID} """)
        results=cursor.fetchone()
        if results is not None:
            classes = ['CLASS1', 'CLASS2', 'CLASS3', 'CLASS4', 'CLASS5']
            nextClass = None

            for i in range(len(results)):
                if results[i] is None:
                    nextClass = classes[i]
                    break

            if nextClass:
                self.conn.queryExecute(f"""UPDATE STUDENT SET {nextClass} = {ClassAdd} WHERE ID = {stuID}""")
                print(f"Course {ClassAdd} added to {nextClass} for student ID {stuID}.")
                if testactive:
                    query_result = self.conn.query(f"""SELECT {nextClass} FROM STUDENT WHERE ID = {stuID}""")
                    for i in query_result:
                        for count, j in enumerate(i):
                            assert str(i[count]) == str(testassert[count + 1]), f'X Results do not match. Expected Value: {testassert[count]}. Actual Value: {i[count]}'
                            print('✔ Test Passed!')    
            else:
                print("No available slot to add the new class.")
        else:
            print(f"No student found with ID {stuID}.")
            #Jared
    
    def addStudent(self):
        highest=0
        #Logic to make ID sequential
        existing_id= self.conn.query(f"SELECT * FROM STUDENT")
        for i in range(len(existing_id)):
            if int(existing_id[i][0]) > highest:
                highest = int(existing_id[i][0])
        id = highest+1
        
        name = input("Enter Name: ")
        surname = input("Enter surname: ")
        email = surname + name[0]
        tempemail=email
        #logic to check that email is still available from both student and instructors emails
        existing_id= self.conn.query("SELECT * FROM STUDENT ")
        existing_id = existing_id + self.conn.query(" SELECT * FROM INSTRUCTOR")
        for i in range(len(existing_id)):
            if existing_id[i][5] == tempemail:
                if not str(existing_id[i][5][-1]).isdigit():
                    tempemail = email+"1"
                else:
                    new_val= int(existing_id[i][5][-1])+1
                    tempemail = f"{email}{new_val}"
        email= tempemail

        gradYear = datetime.now().year + 4
        major = input("Please enter major: ")
        password= input("Please enter a password: ")
        self.conn.queryExecute(f"INSERT INTO STUDENT VALUES('{id}', '{name}', '{surname}', '{gradYear}', '{major}', '{email}','{password}',NULL,NULL,NULL,NULL,NULL)") 
    #Jared
    def removeStudent(self):
        id = input("Please Enter id of Student you wish to remove")
        result  = self.conn.query(f"SELECT * FROM STUDENT WHERE ID = {id}")
        if not len(result)==0:
            self.conn.queryExecute(f"DELETE FROM STUDENT WHERE ID = {id}")
        else :
            print("This student is not within the database")
    #Jared
    def addInstructor(self):
        highest = 0
        #Logic for sequential ID
        existing_id= self.conn.query(f"SELECT * FROM INSTRUCTOR")
        for i in range(len(existing_id)):
            if int(existing_id[i][0]) > highest:
                highest = int(existing_id[i][0])
        id = highest+1  

        name = input("Enter Name: ")
        surname = input("Enter surname: ")
        email = surname + name[0]
        tempemail=email

        #logic to check that email is still available from both student and instructors emails
        existing_id= self.conn.query("SELECT * FROM STUDENT ")
        existing_id = existing_id + self.conn.query(" SELECT * FROM INSTRUCTOR")

        for i in range(len(existing_id)):
            if existing_id[i][5] == tempemail:
                if not str(existing_id[i][5][-1]).isdigit():
                    tempemail = email+"1"
                else:   
                    new_val= int(existing_id[i][5][-1])+1
                    tempemail = f"{email}{new_val}"
        email= tempemail

        title = input("Enter Instrutor's title: ")
        dept = input("Enter instrutor's Department: ")
        password = input("Enter instrutor's password: ")

        #logic to check that email is still available
        hireYear = datetime.now().year
        self.conn.queryExecute(f"INSERT INTO INSTRUCTOR VALUES('{id}', '{name}', '{surname}', '{title}',  '{hireYear}', '{email}','{password}','{dept}')")
    #Jared
    def removeInstructor(self):
        id = input("Please Enter id of Instrutor you wish to remove")
        result  = self.conn.query(f"SELECT * FROM INSTRUTOR WHERE ID = {id}")
        if not len(result)==0:
            self.conn.queryExecute(f"DELETE FROM INSTRUCTOR WHERE ID = {id}")
        else :
            print("This student is not within the database")

    def linkStudent(self, ID, CRN):
        #Implement Logic
        return True

    def linkInstructor(self, ID, CRN):
        #Implement
        return True

#GUI Functions
def showStudentMainpage():
    login_frame.pack_forget()
    remove_course_frame.pack_forget()
    add_course_frame.pack_forget()
    main_student_frame.pack()

def showStudentRemoveClass():
    admin_main_frame.pack_forget()
    remove_course_frame.pack()
    
def showStudentAddClass():
    admin_main_frame.pack_forget()
    add_course_frame.pack()
    
def showAdminMainpage():
    login_frame.pack_forget()
    admin_main_frame.pack()
    
def adminAddStudent():
    admin_main_frame.pack_forget()
    admin_update_frame.pack()
    admin_update_confirm.configure(command=Admin.add_course_student)
    
def adminRemoveStudent():
    admin_main_frame.pack_forget()
    admin_update_frame.pack()
    admin_update_confirm.configure(command=Admin.remove_course_student)
    
def adminBackToMain():
    admin_update_frame.pack_forget()
    admin_main_frame.pack()

def show_signup_page():
    login_frame.pack_forget()
    
def reset_password():
    login_frame.pack_forget()
#Build GUI for WITWorks

global inst, conn

root = tk.Tk()
conn = dbConnection()

root.title("User Authentication System")
root.geometry("400x450")

#Login Frame
login_frame = tk.Frame(root, padx=20, pady=20)
login_frame.pack(fill="both", expand=True)

tk.Label(login_frame, text="Email:", font=("Arial", 12)).grid(row=0, column=0, pady=10, sticky="e")
login_email_entry = tk.Entry(login_frame, font=("Arial", 12))
login_email_entry.grid(row=0, column=1, pady=10)

tk.Label(login_frame, text="Password:", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
login_password_entry = tk.Entry(login_frame, show="*", font=("Arial", 12))
login_password_entry.grid(row=1, column=1, pady=10)

login_button = tk.Button(login_frame, text="Login", command=User.login)
login_button.grid(row=2, column=0, pady=10)

signup_button = tk.Button(login_frame, text="Sign Up", command=show_signup_page)
signup_button.grid(row=2, column=1, pady=10)

reset_button = tk.Button(login_frame, text="Forgot Password", command=reset_password)
reset_button.grid(row=3, columnspan=2, pady=10)



# Student Page GUI Items
main_student_frame = tk.Frame(root, padx=20, pady=20)

print_schedule_button = tk.Button(main_student_frame, text="Print Schedule", command=Student.printSchedule)
print_schedule_button.grid(row=0, column=0, pady=10)

add_course_button = tk.Button(main_student_frame, text="Add Course", command=showStudentAddClass)
add_course_button.grid(row=0, column=1, pady=10)

remove_course_button = tk.Button(main_student_frame, text="Remove Course", command=showStudentRemoveClass)
remove_course_button.grid(row=0, column=2, pady=10)

add_course_button = tk.Button(main_student_frame, text="Add Course", command=showStudentAddClass)

remove_course_frame = tk.Frame(root, padx=20, pady=20)

tk.Label(remove_course_frame, text="Enter CRN", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
remove_course_CRN = tk.Entry(remove_course_frame, font=("Arial", 12))
remove_course_CRN.grid(row=1, column=2, pady=10)

remove_course_back_button = tk.Button(remove_course_frame, text="Back", command=showStudentMainpage)
remove_course_back_button.grid(row=2, column=1, pady=10)

remove_course_submit_button = tk.Button(remove_course_frame, text="Submit Course", command=Student.removeCourse)
remove_course_submit_button.grid(row=2, column=0, pady=10)

add_course_frame = tk.Frame(root, padx=20, pady=20)

tk.Label(add_course_frame, text="Enter CRN", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
add_course_CRN = tk.Entry(add_course_frame, font=("Arial", 12))
add_course_CRN.grid(row=1, column=2, pady=10)

add_course_back_button = tk.Button(add_course_frame, text="Back", command=showStudentMainpage)
add_course_back_button.grid(row=2, column=1, pady=10)

add_course_submit_button = tk.Button(add_course_frame, text="Submit Course", command=Student.addCourse)
add_course_submit_button.grid(row=2, column=0, pady=10)

#Instructor Page GUI Items
inst_main_frame = tk.Frame(root, padx=20, pady=20)

inst_print_schedule_button = tk.Button(inst_main_frame, text="Print Schedule", command=Instructor.print_roster)
inst_print_schedule_button.grid(row=0, column=0, pady=10)


#Admin Page GUI Items
admin_main_frame = tk.Frame(root, padx=20, pady=20)

#main Admin Page
admin_add_course_button = tk.Button(admin_main_frame, text="Add Course", command=adminAddStudent)
admin_add_course_button.grid(row=0, column=1, pady=10)

admin_remove_course_button = tk.Button(admin_main_frame, text="Remove Course", command=adminRemoveStudent)
admin_remove_course_button.grid(row=0, column=2, pady=10)

admin_add_student = tk.Button(admin_main_frame, text="Add Student", command=adminAddStudent)
admin_add_student.grid(row=1, column=1, pady=10)

admin_remove_student = tk.Button(admin_main_frame, text="Remove Student", command=adminRemoveStudent)
admin_remove_student.grid(row=1, column=2, pady=10)

#Update Frame
admin_update_frame = tk.Frame(root, padx=20, pady=20)

tk.Label(admin_update_frame, text="Enter CRN", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
CRN = tk.Entry(admin_update_frame, font=("Arial", 12))
CRN.grid(row=1, column=2, pady=10)

tk.Label(admin_update_frame, text="Enter ID", font=("Arial", 12)).grid(row=2, column=0, pady=10, sticky="e")
ID_NUM = tk.Entry(admin_update_frame, font=("Arial", 12))
ID_NUM.grid(row=2, column=2, pady=10)

admin_update_confirm = tk.Button(admin_update_frame, text="Confirm")
admin_update_confirm.grid(row=3, column=0, pady=10)

admin_update_back = tk.Button(admin_update_frame, text="Back", command=adminBackToMain)
admin_update_back.grid(row=3, column=1, pady=10)

root.mainloop()



