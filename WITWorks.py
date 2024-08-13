import sqlite3
from datetime import datetime
import unittest
import os
import keyboard
from unittest.mock import patch
import time
import tkinter as tk
from tkinter import messagebox



#ClassObjects to be used




#Jared
class dbConnection:
    
    DatabaseURI="LeopardWeb.db"
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
            messagebox.showwarning("FAIL", "INVALID CREDENTIALS")
            
            
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
    
    def time_conflicts():
        studID = stud.ID
        results = conn.queryMany(f"""Select CLASS1,CLASS2,CLASS3,CLASS4,CLASS5 From STUDENT Where ID = '{studID}' """)
        time0 = str(conn.query(f"""Select TIME From COURSE Where CRN = '{results[0][0]}' """))
        time1 = str(conn.query(f"""Select TIME From COURSE Where CRN = '{results[0][1]}' """))
        time2 = str(conn.query(f"""Select TIME From COURSE Where CRN = '{results[0][2]}' """))
        time3 = str(conn.query(f"""Select TIME From COURSE Where CRN = '{results[0][3]}' """))
        time4 = str(conn.query(f"""Select TIME From COURSE Where CRN = '{results[0][4]}' """))
        time0 = ''.join(e  for e in time0 if e.isalnum())
        time1 = ''.join(e  for e in time1 if e.isalnum())
        time2 = ''.join(e  for e in time2 if e.isalnum())
        time3 = ''.join(e  for e in time3 if e.isalnum())
        time4 = ''.join(e  for e in time4 if e.isalnum())

        if time0 == 'None':
            time0 = -3
        if time1 == 'None':
            time1 = -6
        if time2 == 'None':
            time2 = -9
        if time3 == 'None':
            time3 = -12
        if time4 == 'None':
            time4 = -15
        print("---------------------------")
        print("(CLASSES ARE 1:50)")
        print("Times of all 5 classes: ")
        if int(time0) >= 0:
            print("Class 1 starts at " + str(time0))
        if int(time1) >= 0:
           print("Class 2 starts at " + str(time1))
        if int(time2) >= 0:
            print("Class 3 starts at " + str(time2))
        if int(time3) >= 0:
            print("Class 4 starts at " + str(time3))
        if int(time4) >= 0:
            print("Class 5 starts at " + str(time4))
        print("---------------------------")
        conflict = 0
        if (int(time0) == int(time1)) or (int(time0) == int(time2)) or (int(time0) == int(time3)) or (int(time0) == int(time4)):
            print("Time confliction: Class 1 starts at same time as another class.")
            conflict = 1
        if (int(time1) == int(time0)) or (int(time1) == int(time2)) or (int(time1) == int(time3)) or (int(time1) == int(time4)):
            print("Time confliction: Class 2 starts at same time as another class.")
            conflict = 1
        if (int(time2) == int(time1)) or (int(time2) == int(time0)) or (int(time2) == int(time3)) or (int(time2) == int(time4)):
            print("Time confliction: Class 3 starts at same time as another class.")
            conflict = 1
        if (int(time3) == int(time1)) or (int(time3) == int(time2)) or (int(time3) == int(time0)) or (int(time3) == int(time4)):
            print("Time confliction: Class 4 starts at same time as another class.")
            conflict = 1
        if (int(time4) == int(time1)) or (int(time4) == int(time2)) or (int(time4) == int(time3)) or (int(time4) == int(time0)):
            print("Time confliction: Class 5 starts at same time as another class.")
            conflict = 1


        if ((int(time0) + 1) == int(time1)) or ((int(time0) + 1) == int(time2)) or ((int(time0) + 1) == int(time3)) or ((int(time0) + 1) == int(time4)):
            print("Time confliction: Another class begins during Class 1.")
            conflict = 1
        if ((int(time1) + 1) == int(time0)) or ((int(time1) + 1) == int(time2)) or ((int(time1) + 1) == int(time3)) or ((int(time1) + 1) == int(time4)):
            print("Time confliction: Another class begins during Class 2.")
            conflict = 1
        if ((int(time2) + 1) == int(time1)) or ((int(time2) + 1) == int(time0)) or ((int(time2) + 1) == int(time3)) or ((int(time2) + 1) == int(time4)):
            print("Time confliction: Another class begins during Class 3.")
            conflict = 1
        if ((int(time3) + 1) == int(time1)) or ((int(time3) + 1) == int(time2)) or ((int(time3) + 1) == int(time0)) or ((int(time3) + 1) == int(time4)):
            print("Time confliction: Another class begins during Class 4.")
            conflict = 1
        if ((int(time4) + 1) == int(time1)) or ((int(time4) + 1) == int(time2)) or ((int(time4) + 1) == int(time3)) or ((int(time4) + 1) == int(time0)):
            print("Time confliction: Another class begins during Class 5.")
            conflict = 1

        if conflict == 0:
            print("No time conflictons")     
    

    def printSchedule():
        studID = stud.ID
        results = conn.queryMany(f"""Select CLASS1,CLASS2,CLASS3,CLASS4,CLASS5 From STUDENT Where ID = '{studID}' """)
        class1 = str(conn.query(f"""Select TITLE From COURSE Where CRN = '{results[0][0]}' """))
        class2= str(conn.query(f"""Select TITLE From COURSE Where CRN = '{results[0][1]}' """))
        class3 = str(conn.query(f"""Select TITLE From COURSE Where CRN = '{results[0][2]}' """))
        class4 = str(conn.query(f"""Select TITLE From COURSE Where CRN = '{results[0][3]}' """))
        class5 = str(conn.query(f"""Select TITLE From COURSE Where CRN = '{results[0][4]}' """))
        class1 = ''.join(e  for e in class1 if e.isalnum())
        class2 = ''.join(e  for e in class2 if e.isalnum())
        class3 = ''.join(e  for e in class3 if e.isalnum())
        class4 = ''.join(e  for e in class4 if e.isalnum())
        class5 = ''.join(e  for e in class5 if e.isalnum())
        print("Class1 is: " + class1)
        print("Class2 is: " + class2)
        print("Class3 is: " + class3)
        print("Class4 is: " + class4)
        print("Class5 is: " + class5)



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
        addDOW = ClassDOW.get()
        addSemester = ClassSemester.get()
        addYear = ClassYear.get()
        addCredit = ClassCredits.get()
        addTitle = ClassTitle.get()
        addDepartment = ClassDepartment.get()
        addTime = ClassTime.get()
        try:  
            conn.queryExecute(f"INSERT INTO COURSE VALUES({addCRN}, '{addTitle}','{addDepartment}', {addTime}, '{addDOW}', '{addSemester}', {addYear}, {addCredit})") 
            messagebox.showwarning("Sucess",f"Class {addTitle} Successfully added")    
            ClassCRN.delete(0,tk.END)
            ClassTitle.delete(0,tk.END)
            ClassDepartment.delete(0,tk.END)
            ClassTime.delete(0,tk.END)
            ClassDOW.delete(0,tk.END)
            ClassSemester.delete(0,tk.END)
            ClassYear.delete(0,tk.END)
            ClassCredits.delete(0,tk.END)    
            adminBackToMain()
        except:
            messagebox.showwarning("Failure","Please Fill Out all Rows")  
        
            
    def admin_search_filter():
        try:
            filter= SearchCourseType.get().upper()
            search=SearchCourseEntry.get()
            message = f"The Following Courses With The Filter {filter}:{search} Include: "
            results = conn.queryMany(f"SELECT TITLE FROM COURSE WHERE {filter} = '{search}'")
            for i in range(len(results)):
                message =  message + "\n" + results[i][0]
            messagebox.showwarning("Classes",message)    
            adminBackToMain()

        except:
            messagebox.showwarning("Failure",f"Please Enter A Valid Filter Type")    


        
    def remove_course():        #Micah
        
        removeCRN = ClassRemoveCRN.get()
        
        results = conn.query(f"Select TITLE From COURSE Where CRN = '{removeCRN}'")
        if results is None:
            messagebox.showwarning("Failure",f"A Course With CRN {removeCRN} Does Not Exist")
        else:
            conn.queryExecute(f"DELETE FROM COURSE WHERE CRN = {removeCRN}")
            messagebox.showwarning("Success",f"Course With CRN {removeCRN} Deleted")
            ClassRemoveCRN.delete(0,tk.END)
            adminBackToMain()

            
    def remove_course_student():     
        
        stuID = removeStudentClass_ID.get()
        classCRN = removeStudentClass_CRN.get()
        
        results = conn.query(f"Select CLASS1,CLASS2,CLASS3,CLASS4,CLASS5 From STUDENT Where ID = '{stuID}' ")
        
        try:
            conn.queryExecute(f"SELECT NAME FROM STUDENT WHERE ID = {stuID}")
            conn.queryExecute(f"UPDATE STUDENT SET CLASS1 = NULL WHERE CLASS1 = {classCRN} AND ID = {stuID}")
            conn.queryExecute (f"UPDATE STUDENT SET CLASS2 = NULL WHERE CLASS2 = {classCRN} AND ID = {stuID}")
            conn.queryExecute(f"UPDATE STUDENT SET CLASS3 = NULL WHERE CLASS3 = {classCRN} AND ID = {stuID}")
            conn.queryExecute(f"UPDATE STUDENT SET CLASS4 = NULL WHERE CLASS4 = {classCRN} AND ID = {stuID}")
            conn.queryExecute(f"UPDATE STUDENT SET CLASS5 = NULL WHERE CLASS5 = {classCRN} AND ID = {stuID}")
            messagebox.showwarning("Success",f"Course {classCRN} Deleted From {stuID}")
            removeStudentClass_ID.delete(0,tk.END)
            removeStudentClass_CRN.delete(0,tk.END)
            adminBackToMain()
        except:
            messagebox.showwarning("Failure",f"{stuID} Doesn't take {classCRN}")

    def change_instructor_dept():     

        try:
            instID = int(InstructorID_admin.get())
            newDept = newinstructorDept.get()

            conn.queryExecute(f"SELECT NAME FROM INSTRUCTOR WHERE ID = {instID}")
            conn.queryExecute(f"UPDATE INSTRUCTOR SET DEPT = '{newDept}' WHERE ID = {instID}")
            messagebox.showwarning("Success",f"Updated {instID}'s Deparment to {newDept}")
            InstructorID_admin.delete(0,tk.END)
            newinstructorDept.delete(0,tk.END)
            adminBackToMain()
        except:
            messagebox.showwarning("Failure","Please Enter Valid Instructor ID")

              


    def add_course_student():               #Micah
        stuID = addStudentClass_ID.get()
        ClassAdd = addStudentClass_CRN.get()
   

        results = conn.query(f"""Select CLASS1,CLASS2,CLASS3,CLASS4,CLASS5 From STUDENT Where ID = {stuID} """)
        if results is not None:
            classes = ['CLASS1', 'CLASS2', 'CLASS3', 'CLASS4', 'CLASS5']
            nextClass = None

            for i in range(len(results)):
                if results[i] is None:
                    nextClass = classes[i]
                    break

            if nextClass:
                conn.queryExecute(f"""UPDATE STUDENT SET {nextClass} = {ClassAdd} WHERE ID = {stuID}""")
                messagebox.showwarning("Success",f"{ClassAdd} Added To {stuID}'s Schedule")
                addStudentClass_ID.delete(0,tk.END)
                addStudentClass_CRN.delete(0,tk.END)
                adminBackToMain()

            else:
              messagebox.showwarning("Failure",f" {stuID}'s Schedule Is Full")
        else:
            messagebox.showwarning("Fallure",f"No Student With ID {stuID} Exists")
            #Jared
   
    



    
    def addStudent():
        highest=0
        #Logic to make ID sequential
        existing_id= conn.queryMany("SELECT ID FROM STUDENT")
        for i in range(len(existing_id)):
            if existing_id[i][0] > highest:
                highest = existing_id[i][0]
        id = highest+1
        
        name = addStudentName.get()
        surname = addStudentSurname.get()
        email = surname + name[0]
        tempemail=email
     
        #logic to check that email is still available from both student and instructors emails
        existing_id= conn.queryMany("SELECT EMAIL FROM USERS")
        for i in range(len(existing_id)):
            if existing_id[i][0] == tempemail:
                if not str(existing_id[i][0][-1]).isdigit():
                    tempemail = email+"1"
                else:
                    new_val= int(existing_id[i][0][-1])+1
                    tempemail = f"{email}{new_val}"
        email= tempemail

        gradYear = datetime.now().year + 4
        major = addStudentMajor.get()
        password= addStudentPassword.get()
        try:
            conn.queryExecute(f"INSERT INTO STUDENT VALUES('{id}', '{name}', '{surname}', '{gradYear}', '{major}', '{email}','{password}',NULL,NULL,NULL,NULL,NULL)")
            conn.queryExecute(f"INSERT INTO USERS VALUES ('{id}', '{name}', '{surname}', 'STUDENT', '{email}' , '{password}')") 
            messagebox.showwarning("Success", f"{name} Sucessfully Added")
            addStudentName.delete(0,tk.END)
            addStudentSurname.delete(0,tk.END)
            addStudentMajor.delete(0,tk.END)
            addStudentPassword.delete(0,tk.END)
            adminBackToMain()

        except:
            messagebox.showwarning("Fail", "Failed To Add User")

    
    def removeStudent():
        id = removeStudentID.get()

        result  = conn.query(f"SELECT * FROM STUDENT WHERE ID = {id}")
        if result is not None:
            conn.queryExecute(f"DELETE FROM STUDENT WHERE ID = {id}")
            conn.queryExecute(f"DELETE FROM USERS WHERE ID = {id}")
            messagebox.showwarning("SUCCESS", "STUDENT DELETED")
            removeStudentID.delete(0,tk.END)
            adminBackToMain()
        else:
            messagebox.showwarning("FAIL", f"Student With ID {id}Does Not Exist")
  

    #Jared
    def addInstructor():
        highest = 0
        #Logic for sequential ID
        existing_id= conn.queryMany(f"SELECT ID FROM INSTRUCTOR")
        for i in range(len(existing_id)):
            if int(existing_id[i][0]) > highest:
                highest = int(existing_id[i][0])
        id = highest+1  

        name = addInstructorName.get()
        surname = addInstructorSurname.get()
        dept = addInstructorDepartment.get()
        title= addInstructorTitle.get()
        password=addInstructorPassword.get()
        email = surname + name[0]
        tempemail=email

        #logic to check that email is still available from both student and instructors emails
        existing_id= conn.queryMany("SELECT EMAIL FROM USERS")

        for i in range(len(existing_id)):
            if existing_id[i][0] == tempemail:
                if not str(existing_id[i][0][-1]).isdigit():
                    tempemail = email+"1"
                else:   
                    new_val= int(existing_id[i][0][-1])+1
                    tempemail = f"{email}{new_val}"
        email= tempemail

        #logic to check that email is still available
        hireYear = datetime.now().year
        try:
            conn.queryExecute(f"INSERT INTO INSTRUCTOR VALUES('{id}', '{name}', '{surname}', '{title}',  '{hireYear}', '{dept}','{email}','{password}')")
            conn.queryExecute(f"INSERT INTO USERS VALUES('{id}', '{name}', '{surname}', 'INSTRUCTOR','{email}','{password}')")

            messagebox.showwarning("SUCCESS", f"Instructor {name} Added")     
            name = addInstructorName.delete(0,tk.END)
            surname = addInstructorSurname.delete(0,tk.END)
            department = addInstructorDepartment.delete(0,tk.END)
            title= addInstructorTitle.delete(0,tk.END)
            password=addInstructorPassword.delete(0,tk.END)
            adminBackToMain()
        except:
            messagebox.showwarning("FAIL", "Invalid Inputs")


    #Jared
    def removeInstructor():
        id = removeInstructorID.get()

        result  = conn.query(f"SELECT * FROM Instructor WHERE ID = {id}")
        if result is not None:
            conn.queryExecute(f"DELETE FROM Instructor WHERE ID = {id}")
            conn.queryExecute(f"DELETE FROM USERS WHERE ID = {id}")
            messagebox.showwarning("SUCCESS", f"Instructor {id} Deleted")
            removeInstructorID.delete(0,tk.END)
            adminBackToMain()
        else:
            messagebox.showwarning("FAIL", f"Instructor with ID {id} Does Not Exist")

    

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
    #Admin.remove_course()
    admin_remove_class_confirm.configure(command=Admin.remove_course)
    
def adminAddStudent():
    admin_main_frame.pack_forget()
    admin_addStudent_frame.pack()
    #Admin.addStudent()
    admin_update_confirm_add.configure(command=Admin.addStudent)
    
def adminRemoveStudent():
    admin_main_frame.pack_forget()
    admin_removeStudent_frame.pack()
    #Admin.removeStudent()
    admin_update_confirm_remove.configure(command=Admin.removeStudent)
    
def adminAddInstructor():
    admin_main_frame.pack_forget()
    admin_addInstructor_frame.pack()
    admin_Instructor_add.configure(command=Admin.addInstructor)
    
def adminRemoveInstructor():
    admin_main_frame.pack_forget()
    admin_removeInstructor_frame.pack()
    admin_Instructor_remove.configure(command=Admin.removeInstructor)

def adminAddStudentCourse():
    admin_main_frame.pack_forget()
    addStudentClass_frame.pack()
    addStudentClass_confirm.configure(command=Admin.add_course_student)
    
    
def adminRemoveStudentCourse():
    admin_main_frame.pack_forget()
    removeStudentClass_frame.pack()
    removeStudentClass_confirm.configure(command=Admin.remove_course_student)
    
def adminChangeInstructorDept():
    admin_main_frame.pack_forget()
    change_dept_instructor_frame.pack()
    newinstructorDept_confirm.configure(command=Admin.change_instructor_dept)

def adminSearchCourses():
    admin_main_frame.pack_forget()
    search_course_frame.pack()
    search_course_frame_confirm.configure(command=Admin.admin_search_filter)



def adminBackToMain():
    admin_addInstructor_frame.pack_forget()
    admin_remove_class_frame.pack_forget()
    admin_add_class_frame.pack_forget()
    admin_addStudent_frame.pack_forget()
    addStudentClass_frame.pack_forget()
    removeStudentClass_frame.pack_forget()
    admin_removeStudent_frame.pack_forget()
    change_dept_instructor_frame.pack_forget()
    search_course_frame.pack_forget()
    admin_main_frame.pack()
    admin_removeInstructor_frame.pack_forget()

def ReturnToLogin():
    admin_addInstructor_frame.pack_forget()
    admin_remove_class_frame.pack_forget()
    admin_add_class_frame.pack_forget()
    admin_addStudent_frame.pack_forget()
    addStudentClass_frame.pack_forget()
    removeStudentClass_frame.pack_forget()
    admin_removeStudent_frame.pack_forget()
    login_frame.pack()
    admin_main_frame.pack_forget()
    admin_removeInstructor_frame.pack_forget()
    main_student_frame.pack_forget()



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





# Student Page GUI Items
main_student_frame = tk.Frame(root, padx=20, pady=20)

print_schedule_button = tk.Button(main_student_frame, text="Print Schedule", command=Student.printSchedule)
print_schedule_button.grid(row=0, column=0, pady=10)

add_course_button = tk.Button(main_student_frame, text="Add Course", command=showStudentAddClass)
add_course_button.grid(row=0, column=1, pady=10)

remove_course_button = tk.Button(main_student_frame, text="Remove Course", command=showStudentRemoveClass)
remove_course_button.grid(row=0, column=2, pady=10)

check_conflicts_button = tk.Button(main_student_frame, text="Check Time Conflicts", command=Student.time_conflicts)
check_conflicts_button.grid(row=0, column=3, pady=10)

student_back_Button = tk.Button(main_student_frame, text="Back", command=ReturnToLogin)
student_back_Button.grid(row=10, column=2, pady=10)


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

admin_add_student_course = tk.Button(admin_main_frame, text="Add Student to Class", command=adminAddStudentCourse)
admin_add_student_course.grid(row=2, column=1, pady=10)

admin_remove_student_course = tk.Button(admin_main_frame, text="Remove Student from Class", command=adminRemoveStudentCourse)
admin_remove_student_course.grid(row=2, column=2, pady=10)

admin_add_Instructor = tk.Button(admin_main_frame, text="Add Instructor", command=adminAddInstructor)
admin_add_Instructor.grid(row=3, column=1, pady=10)

admin_remove_Instructor = tk.Button(admin_main_frame, text="Remove Instructor", command=adminRemoveInstructor)
admin_remove_Instructor.grid(row=3, column=2, pady=10)

admin_change_instructor_dept = tk.Button(admin_main_frame, text="Change Instructor Dept", command=adminChangeInstructorDept)
admin_change_instructor_dept.grid(row=4, column=1, pady=10)

admin_filter_search = tk.Button(admin_main_frame, text="Change Instructor Dept", command=adminSearchCourses)
admin_filter_search.grid(row=4, column=2, pady=10)

tk.Label(admin_main_frame,text="").grid(column=3,row=4)
tk.Label(admin_main_frame,text="").grid(column=1,row=5)
tk.Label(admin_main_frame,text="").grid(column=1,row=6)
tk.Label(admin_main_frame,text="").grid(column=1,row=7)
tk.Label(admin_main_frame,text="").grid(column=1,row=8)
tk.Label(admin_main_frame,text="").grid(column=1,row=9)


admin_back_Button = tk.Button(admin_main_frame, text="Back", command=ReturnToLogin)
admin_back_Button.grid(row=10, column=2, pady=10)

#Admin Update Class
admin_remove_class_frame = tk.Frame(root, padx=20, pady=20)

tk.Label(admin_remove_class_frame, text="CRN", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
ClassRemoveCRN = tk.Entry(admin_remove_class_frame, font=("Arial", 12))
ClassRemoveCRN.grid(row=1, column=2, pady=10)

admin_remove_class_confirm = tk.Button(admin_remove_class_frame, text="Confirm",command= adminRemoveCourse)
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




admin_add_class_confirm = tk.Button(admin_add_class_frame, text="Confirm",command=adminAddCourse)
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


admin_update_confirm_add = tk.Button(admin_addStudent_frame, text="Confirm", command =adminAddStudent)
admin_update_confirm_add.grid(row=5, column=0, pady=10)

admin_update_back = tk.Button(admin_addStudent_frame, text="Back", command=adminBackToMain)
admin_update_back.grid(row=5, column=1, pady=10)


#REMOVE STUDENT FRAME
admin_removeStudent_frame = tk.Frame(root, padx=20, pady=20)

tk.Label(admin_removeStudent_frame, text="ID", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
removeStudentID = tk.Entry(admin_removeStudent_frame, font=("Arial", 12))
removeStudentID.grid(row=1, column=2, pady=10)

admin_update_confirm_remove = tk.Button(admin_removeStudent_frame, text="Confirm",command= adminRemoveStudent)
admin_update_confirm_remove.grid(row=2, column=0, pady=10)

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

tk.Label(admin_addInstructor_frame, text="Department", font=("Arial", 12)).grid(row=4, column=0, pady=10, sticky="e")
addInstructorDepartment = tk.Entry(admin_addInstructor_frame, font=("Arial", 12))
addInstructorDepartment.grid(row=4, column=2, pady=10)

tk.Label(admin_addInstructor_frame, text="Title", font=("Arial", 12)).grid(row=5, column=0, pady=10, sticky="e")
addInstructorTitle = tk.Entry(admin_addInstructor_frame, font=("Arial", 12))
addInstructorTitle.grid(row=5, column=2, pady=10)



admin_Instructor_add = tk.Button(admin_addInstructor_frame, text="Confirm",command=adminAddInstructor)
admin_Instructor_add.grid(row=6, column=0, pady=10)

admin_Instructor_update_back = tk.Button(admin_addInstructor_frame, text="Back", command=adminBackToMain)
admin_Instructor_update_back.grid(row=6, column=1, pady=10)


#REMOVE INSTRUCTOR FRAME
admin_removeInstructor_frame = tk.Frame(root, padx=20, pady=20)

tk.Label(admin_removeInstructor_frame, text="ID", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
removeInstructorID = tk.Entry(admin_removeInstructor_frame, font=("Arial", 12))
removeInstructorID.grid(row=1, column=2, pady=10)

admin_Instructor_remove = tk.Button(admin_removeInstructor_frame, text="Confirm",command= adminRemoveInstructor)
admin_Instructor_remove.grid(row=2, column=0, pady=10)

admin_update_back = tk.Button(admin_removeInstructor_frame, text="Back", command=adminBackToMain)
admin_update_back.grid(row=2, column=1, pady=10)


addStudentClass_frame = tk.Frame(root, padx=20, pady=20 )

tk.Label(addStudentClass_frame, text="ID", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
addStudentClass_ID = tk.Entry(addStudentClass_frame, font=("Arial", 12))
addStudentClass_ID.grid(row=1, column=2, pady=10)

tk.Label(addStudentClass_frame, text="CRN", font=("Arial", 12)).grid(row=2, column=0, pady=10, sticky="e")
addStudentClass_CRN = tk.Entry(addStudentClass_frame, font=("Arial", 12))
addStudentClass_CRN.grid(row=2, column=2, pady=10)

addStudentClass_confirm = tk.Button(addStudentClass_frame, text="Confirm",command=adminAddStudentCourse)
addStudentClass_confirm.grid(row=3, column=0, pady=10)

addStudentClass_back = tk.Button(addStudentClass_frame, text="Back", command=adminBackToMain)
addStudentClass_back.grid(row=3, column=1, pady=10)

#remove student course
removeStudentClass_frame = tk.Frame(root, padx=20, pady=20 )

tk.Label(removeStudentClass_frame, text="ID", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
removeStudentClass_ID = tk.Entry(removeStudentClass_frame, font=("Arial", 12))
removeStudentClass_ID.grid(row=1, column=2, pady=10)

tk.Label(removeStudentClass_frame, text="CRN", font=("Arial", 12)).grid(row=2, column=0, pady=10, sticky="e")
removeStudentClass_CRN = tk.Entry(removeStudentClass_frame, font=("Arial", 12))
removeStudentClass_CRN.grid(row=2, column=2, pady=10)

removeStudentClass_confirm = tk.Button(removeStudentClass_frame, text="Confirm",command=adminRemoveStudentCourse)
removeStudentClass_confirm.grid(row=3, column=0, pady=10)

removeStudentClass_back = tk.Button(removeStudentClass_frame, text="Back", command=adminBackToMain)
removeStudentClass_back.grid(row=3, column=1, pady=10)

#instructor thjing
change_dept_instructor_frame = tk.Frame(root, padx=20, pady=20 )

tk.Label(change_dept_instructor_frame, text="Instructor ID", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
InstructorID_admin = tk.Entry(change_dept_instructor_frame, font=("Arial", 12))
InstructorID_admin.grid(row=1, column=2, pady=10)

tk.Label(change_dept_instructor_frame, text="New Department", font=("Arial", 12)).grid(row=2, column=0, pady=10, sticky="e")
newinstructorDept = tk.Entry(change_dept_instructor_frame, font=("Arial", 12))
newinstructorDept.grid(row=2, column=2, pady=10)

newinstructorDept_confirm = tk.Button(change_dept_instructor_frame, text="Confirm",command=adminRemoveStudentCourse)
newinstructorDept_confirm.grid(row=3, column=0, pady=10)

removeStudentClass_back = tk.Button(change_dept_instructor_frame, text="Back", command=adminBackToMain)
removeStudentClass_back.grid(row=3, column=1, pady=10)

#Serch Courses
search_course_frame = tk.Frame(root, padx=20, pady=20 )

tk.Label(search_course_frame, text="Please Enter A Filter Type and a Value", font=("Arial", 12)).grid(row=0, columnspan=3, pady=10, sticky="w")
tk.Label(search_course_frame, text="CASE SENSETIVE", font=("Arial", 12)).grid(row=1, columnspan=3, pady=10, sticky="w")
tk.Label(search_course_frame, text="Search Filter", font=("Arial", 12)).grid(row=3, column=0, pady=10, sticky="e")
SearchCourseType = tk.Entry(search_course_frame, font=("Arial", 12))
SearchCourseType.grid(row=3, column=2, pady=10)

tk.Label(search_course_frame, text="Search", font=("Arial", 12)).grid(row=4, column=0, pady=10, sticky="e")
SearchCourseEntry = tk.Entry(search_course_frame, font=("Arial", 12))
SearchCourseEntry.grid(row=4, column=2, pady=10)


search_course_frame_confirm = tk.Button(search_course_frame, text="Confirm",command=adminSearchCourses)
search_course_frame_confirm.grid(row=5, column=0, pady=10)

removeStudentClass_back = tk.Button(search_course_frame, text="Back", command=adminBackToMain)
removeStudentClass_back.grid(row=5, column=1, pady=10)



root.mainloop()


