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
        
    def queryMany(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()
    
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
        
    def add_course():       #Micah
        addCRN = ClassCRN.get()
        results = conn.query(f"""Select TITLE From COURSE Where CRN = {addCRN} """)
        if results is None:
          #  testinputs = ["Hi", "CS", 10, "Thu", "Summer", 2021, 3]

            departments = ["BSCO", "BSEE", "HUSS", "BSME", "BSBE"]
            semesters = ["Fall", "Summer", "Spring"]
            Credits = ["2", "3", "4"]


            addTitle = ClassTitle.get()
            addDepartment = ClassDepartment.get()
            if (addDepartment not in departments):
                messagebox.showerror("Invalid Department Type")
                return
            addTime = ClassTime.get()
            if not addTime.isnumeric():
                messagebox.showerror("Invalid Input")
            addDOW = ClassDOW.get()
            addSemester = ClassSemester.get()
            if (addSemester not in semesters):
                messagebox.showerror("Invalid Semester Type")
                return
            addYear = ClassYear.get()
            if not addYear.isnumeric():
                messagebox.showerror("Invalid Input")
            addCredit = ClassCredits.get()
            if addCredit not in Credits:
                messagebox.showerror("Invalid Credit Amount")
                
            conn.queryExecute(f"INSERT INTO COURSE VALUES({addCRN}, '{addTitle}','{addDepartment}', {addTime}, '{addDOW}', '{addSemester}', {addYear}, {addCredit})") 
        else:
            print("Course already has that CRN")
            
        adminBackToMain()
        
    def remove_course():        #Micah
        
        removeCRN = ClassRemoveCRN.get()
        
        results = conn.query(f"Select TITLE From COURSE Where CRN = '{removeCRN}'")
        if results is None:
            print("A course with that CRN does not exist")
        else:
            conn.queryExecute(f"DELETE FROM COURSE WHERE CRN = {removeCRN}")
            
        adminBackToMain()
            
    def remove_course_student(self):     
        
        stuID = ID_NUM.get()
        classCRN = CRN.get()
        
        results = conn.query(f"Select CLASS1,CLASS2,CLASS3,CLASS4,CLASS5 From STUDENT Where ID = '{stuID}' ")
        
        for i in results:
            print("The courses being taken are:")
            print(i)
        removeclass =input("Which course do you want to remove?")
        conn.queryExecute(f"UPDATE STUDENT SET CLASS1 = NULL WHERE CLASS1 = {removeclass} AND ID = {stuID}")
        conn.queryExecute (f"UPDATE STUDENT SET CLASS2 = NULL WHERE CLASS2 = {removeclass} AND ID = {stuID}")
        conn.queryExecute(f"UPDATE STUDENT SET CLASS3 = NULL WHERE CLASS3 = {removeclass} AND ID = {stuID}")
        conn.queryExecute(f"UPDATE STUDENT SET CLASS4 = NULL WHERE CLASS4 = {removeclass} AND ID = {stuID}")
        conn.queryExecute(f"UPDATE STUDENT SET CLASS5 = NULL WHERE CLASS5 = {removeclass} AND ID = {stuID}")

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
    
    def addStudent():
        highest=0
        #Logic to make ID sequential
        existing_id= conn.queryMany("SELECT ID FROM USERS")
        for i in range(len(existing_id)):
            if existing_id[i][0] > highest:
                highest = existing_id[i][0]
        id = highest+1
        
        name = addStudentName.get()
        surname = addStudentSurname.get()
        email = surname + name[0]
        tempemail=email
        #logic to check that email is still available from both student and instructors emails
        existing_id= conn.query("SELECT EMAIL FROM USERS")
        for i in range(len(existing_id)):
            if existing_id[i][0] == tempemail:
                if not str(existing_id[i][0][-1]).isdigit():
                    tempemail = email+"1"
                else:
                    new_val= int(existing_id[i][5][-1])+1
                    tempemail = f"{email}{new_val}"
        email= tempemail

        gradYear = datetime.now().year + 4
        major = addStudentMajor.get()
        password= addStudentPassword.get()
        conn.queryExecute(f"INSERT INTO STUDENT VALUES('{id}', '{name}', '{surname}', '{gradYear}', '{major}', '{email}','{password}',NULL,NULL,NULL,NULL,NULL)")
        conn.queryExecute(f"INSERT INTO USERS VALUES ('{id}', '{name}', '{surname}', 'STUDENT', '{email}' , '{password}')") 
        adminBackToMain()
    
    def removeStudent():
        id = removeStudentID.get()
        result  = conn.query(f"SELECT * FROM STUDENT WHERE ID = {id}")
        if result is not None:
            conn.queryExecute(f"DELETE FROM STUDENT WHERE ID = {id}")
            conn.queryExecute(f"DELETE FROM USERS WHERE ID = {id}")
        else:
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
    def removeInstructor():
        id = removeInstructorID.get()
        result  = conn.query(f"SELECT * FROM INSTRUTOR WHERE ID = '{id}'")
        if result is not None:
            conn.queryExecute(f"DELETE FROM INSTRUCTOR WHERE ID = '{id}'")
            conn.queryExecute(f"DELETE FROM USERS WHERE ID = '{id}'")
        else :
            print("This student is not within the database")

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
    admin_add_class_frame.pack_forget()
    admin_remove_class_frame.pack_forget()
    admin_addStudent_frame.pack_forget()
    admin_main_frame.pack()
    
def adminAddCourse():
    admin_main_frame.pack_forget()
    admin_add_class_frame.pack()
    admin_add_class_confirm.configure(command=Admin.add_course)
    
def adminRemoveCourse():
    admin_main_frame.pack_forget()
    admin_remove_class_frame.pack()
    admin_remove_class_confirm.configure(command=Admin.remove_course)
    
def adminAddStudent():
    admin_main_frame.pack_forget()
    admin_addStudent_frame.pack()
    admin_update_confirm.configure(command=Admin.addStudent)
    
def adminRemoveStudent():
    admin_main_frame.pack_forget()
    admin_removeStudent_frame.pack()
    admin_update_confirm.configure(command=Admin.removeStudent)
    
def adminAddInstructor():
    admin_main_frame.pack_forget()
    admin_addInstructor_frame.pack()
    admin_Instructor_update_confirm.configure(command=Admin.addInstructor)
    
def adminRemoveInstructor():
    admin_main_frame.pack_forget()
    admin_removeInstructor_frame.pack()
    admin_Instructor_update_confirm.configure(command=Admin.removeInstructor)
    
def adminBackToMain():
    admin_remove_class_frame.pack_forget()
    admin_add_class_frame.pack_forget()
    admin_addStudent_frame.pack_forget()
    admin_removeStudent_frame.pack_forget()
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
admin_add_course_button = tk.Button(admin_main_frame, text="Add Course", command=adminAddCourse)
admin_add_course_button.grid(row=0, column=1, pady=10)

admin_remove_course_button = tk.Button(admin_main_frame, text="Remove Course", command=adminRemoveCourse)
admin_remove_course_button.grid(row=0, column=2, pady=10)

admin_add_student = tk.Button(admin_main_frame, text="Add Student", command=adminAddStudent)
admin_add_student.grid(row=1, column=1, pady=10)

admin_remove_student = tk.Button(admin_main_frame, text="Remove Student", command=adminRemoveStudent)
admin_remove_student.grid(row=1, column=2, pady=10)

admin_add_Instructor = tk.Button(admin_main_frame, text="Add Student", command=adminAddStudent)
admin_add_Instructor.grid(row=2, column=1, pady=10)

admin_remove_Instructor = tk.Button(admin_main_frame, text="Remove Student", command=adminRemoveStudent)
admin_remove_Instructor.grid(row=2, column=2, pady=10)

#Admin Update Class
admin_remove_class_frame = tk.Frame(root, padx=20, pady=20)

tk.Label(admin_remove_class_frame, text="CRN", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
ClassRemoveCRN = tk.Entry(admin_remove_class_frame, font=("Arial", 12))
ClassRemoveCRN.grid(row=1, column=2, pady=10)

admin_remove_class_confirm = tk.Button(admin_remove_class_frame, text="Confirm")
admin_remove_class_confirm.grid(row=2, column=1, pady=10)

admin_remove_class_back = tk.Button(admin_remove_class_frame, text="Back", command=adminBackToMain)
admin_remove_class_back.grid(row=2, column=2, pady=10)




admin_add_class_frame = tk.Frame(root, padx=20, pady=20)

tk.Label(admin_add_class_frame, text="CRN", font=("Arial", 12)).grid(row=0, column=0, pady=10, sticky="e")
ClassCRN = tk.Entry(admin_add_class_frame, font=("Arial", 12))
ClassCRN.grid(row=0, column=2, pady=10)

tk.Label(admin_add_class_frame, text="Title", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
ClassTitle = tk.Entry(admin_add_class_frame, font=("Arial", 12))
ClassTitle.grid(row=1, column=2, pady=10)

tk.Label(admin_add_class_frame, text="Department", font=("Arial", 12)).grid(row=2, column=0, pady=10, sticky="e")
ClassDepartment = tk.Entry(admin_add_class_frame, font=("Arial", 12))
ClassDepartment.grid(row=2, column=2, pady=10)

tk.Label(admin_add_class_frame, text="Class Time", font=("Arial", 12)).grid(row=3, column=0, pady=10, sticky="e")
ClassTime = tk.Entry(admin_add_class_frame, font=("Arial", 12))
ClassTime.grid(row=3, column=2, pady=10)

tk.Label(admin_add_class_frame, text="DOW", font=("Arial", 12)).grid(row=4, column=0, pady=10, sticky="e")
ClassDOW = tk.Entry(admin_add_class_frame, font=("Arial", 12))
ClassDOW.grid(row=4, column=2, pady=10)

tk.Label(admin_add_class_frame, text="Semester", font=("Arial", 12)).grid(row=5, column=0, pady=10, sticky="e")
ClassSemester = tk.Entry(admin_add_class_frame, font=("Arial", 12))
ClassSemester.grid(row=5, column=2, pady=10)

tk.Label(admin_add_class_frame, text="Year", font=("Arial", 12)).grid(row=6, column=0, pady=10, sticky="e")
ClassYear = tk.Entry(admin_add_class_frame, font=("Arial", 12))
ClassYear.grid(row=6, column=2, pady=10)

tk.Label(admin_add_class_frame, text="Credits", font=("Arial", 12)).grid(row=7, column=0, pady=10, sticky="e")
ClassCredits = tk.Entry(admin_add_class_frame, font=("Arial", 12))
ClassCredits.grid(row=7, column=2, pady=10)






admin_add_class_confirm = tk.Button(admin_add_class_frame, text="Confirm")
admin_add_class_confirm.grid(row=8, column=1, pady=10)

admin_add_class_back = tk.Button(admin_add_class_frame, text="Back", command=adminBackToMain)
admin_add_class_back.grid(row=8, column=2, pady=10)



#ADD STUDENT FRAME
admin_addStudent_frame = tk.Frame(root, padx=20, pady=20)

tk.Label(admin_addStudent_frame, text="Name", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
addStudentName = tk.Entry(admin_addStudent_frame, font=("Arial", 12))
addStudentName.grid(row=1, column=2, pady=10)

tk.Label(admin_addStudent_frame, text="Surname", font=("Arial", 12)).grid(row=2, column=0, pady=10, sticky="e")
addStudentSurname = tk.Entry(admin_addStudent_frame, font=("Arial", 12))
addStudentSurname.grid(row=2, column=2, pady=10)

tk.Label(admin_addStudent_frame, text="Password", font=("Arial", 12)).grid(row=3, column=0, pady=10, sticky="e")
addStudentPassword = tk.Entry(admin_addStudent_frame, font=("Arial", 12))
addStudentPassword.grid(row=3, column=2, pady=10)

tk.Label(admin_addStudent_frame, text="Major", font=("Arial", 12)).grid(row=4, column=0, pady=10, sticky="e")
addStudentMajor = tk.Entry(admin_addStudent_frame, font=("Arial", 12))
addStudentMajor.grid(row=4, column=2, pady=10)


admin_update_confirm = tk.Button(admin_addStudent_frame, text="Confirm")
admin_update_confirm.grid(row=5, column=0, pady=10)

admin_update_back = tk.Button(admin_addStudent_frame, text="Back", command=adminBackToMain)
admin_update_back.grid(row=5, column=1, pady=10)


#REMOVE STUDENT FRAME
admin_removeStudent_frame = tk.Frame(root, padx=20, pady=20)

tk.Label(admin_removeStudent_frame, text="ID", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
removeStudentID = tk.Entry(admin_removeStudent_frame, font=("Arial", 12))
removeStudentID.grid(row=1, column=2, pady=10)

admin_update_confirm = tk.Button(admin_removeStudent_frame, text="Confirm")
admin_update_confirm.grid(row=2, column=0, pady=10)

admin_update_back = tk.Button(admin_removeStudent_frame, text="Back", command=adminBackToMain)
admin_update_back.grid(row=2, column=1, pady=10)





admin_addInstructor_frame = tk.Frame(root, padx=20, pady=20)

tk.Label(admin_addInstructor_frame, text="Name", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
addInstructorName = tk.Entry(admin_addInstructor_frame, font=("Arial", 12))
addInstructorName.grid(row=1, column=2, pady=10)

tk.Label(admin_addInstructor_frame, text="Surname", font=("Arial", 12)).grid(row=2, column=0, pady=10, sticky="e")
addInstructorSurname = tk.Entry(admin_addInstructor_frame, font=("Arial", 12))
addInstructorSurname.grid(row=2, column=2, pady=10)

tk.Label(admin_addInstructor_frame, text="Password", font=("Arial", 12)).grid(row=3, column=0, pady=10, sticky="e")
addInstructorPassword = tk.Entry(admin_addInstructor_frame, font=("Arial", 12))
addInstructorPassword.grid(row=3, column=2, pady=10)

tk.Label(admin_addInstructor_frame, text="Major", font=("Arial", 12)).grid(row=4, column=0, pady=10, sticky="e")
addInstructorMajor = tk.Entry(admin_addInstructor_frame, font=("Arial", 12))
addInstructorMajor.grid(row=4, column=2, pady=10)


admin_Instructor_update_confirm = tk.Button(admin_addInstructor_frame, text="Confirm")
admin_Instructor_update_confirm.grid(row=5, column=0, pady=10)

admin_Instructor_update_back = tk.Button(admin_addInstructor_frame, text="Back", command=adminBackToMain)
admin_Instructor_update_back.grid(row=5, column=1, pady=10)


#REMOVE STUDENT FRAME
admin_removeInstructor_frame = tk.Frame(root, padx=20, pady=20)

tk.Label(admin_removeInstructor_frame, text="ID", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
removeInstructorID = tk.Entry(admin_removeInstructor_frame, font=("Arial", 12))
removeInstructorID.grid(row=1, column=2, pady=10)

admin_update_confirm = tk.Button(admin_removeInstructor_frame, text="Confirm")
admin_update_confirm.grid(row=2, column=0, pady=10)

admin_update_back = tk.Button(admin_removeInstructor_frame, text="Back", command=adminBackToMain)
admin_update_back.grid(row=2, column=1, pady=10)




root.mainloop()



