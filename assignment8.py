import sqlite3
from datetime import datetime
import unittest
import os
from unittest.mock import patch
import keyboard
import time

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
        return self.cur.fetchall()
    
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
    
    #SQL Database Access Objects
    conn = dbConnection()
    #Jared
    def login(self):
        Email = input("Enter your Email")
        password = input("Enter your Passsword")
        query = "SELECT * FROM USERS WHERE Email = '" + Email + "' AND Password = '" + password +"'"
        results = self.conn.query(query)
        if (results is not None):
            self.Email = Email
            query = "SELECT Name FROM USERS WHERE Email = '" + Email + "' AND Password = '" + password +"'"
            self.name = self.conn.query(query)
            query = "SELECT Surname FROM USERS WHERE Email = '" + Email + "' AND Password = '" + password +"'"
            self.Surname = self.conn.query(query)
            query = "SELECT ID FROM USERS WHERE Email = '" + Email + "' AND Password = '" + password +"'"
            self.ID = self.conn.query(query)
        else :
            print("Invalid Credentials")
            
            
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
    
    GradYear=None
    Major=None
    #Dictionary where key is CRN Value is Final Grade
    TakenCourses=None
    #Dictionary where key is CRN value is array of cource info
    #Or Array of CRN Values
    RegisteredCourses=None
    
    def __init__(self, in_name):
        self.sur_name = in_name

    #Jared
    def addCourse(self, CRN):
         #Check if CRN exists
        CRN = input("Enter the CRN of the class you wish to add")
        
        results = self.conn.query(f"SELECT * FROM COURSE WHERE CRN = '{CRN}'")
        if (results is not None):
            #Need logic to check if credits match
            row =  list(self.conn.query(f"SELECT CLASS1, CLASS2, CLASS3, CLASS4, CLASS5 FROM STUDENT WHERE ID = '{self.ID}'"))
            for i in range(5):
                if row[0][i] is None:
                    self.conn.queryExecute(f"UPDATE STUDENT SET CLASS{i+1} = '{CRN}' WHERE ID = '{self.ID}'")
                    print("Class has been updated")
                    break

    #Jared
    def removeCourse(self, CRN):
        #Check if CRN exists
        CRN = input("Enter the CRN of the class you wish to add")
        
        results = self.conn.query(f"SELECT * FROM COURSE WHERE CRN = '{CRN}'")
        if (results is not None):
            #Need logic to check if credits match
            row =  list(self.conn.query(f"SELECT CLASS1, CLASS2, CLASS3, CLASS4, CLASS5 FROM STUDENT WHERE ID = '{self.ID}'"))
            for i in range(5):
                if row[0][i] == CRN:
                    self.conn.queryExecute(f"UPDATE STUDENT SET CLASS{i+1} = 'NONE' WHERE ID = '{self.ID}'")
            
    def checkConflict(self):
        results = self.conn.query("SELECT REGISTEREDCOURSES FROM STUDENTS WHERE EMAIL = '" + self.Email+ "'")
        for row in results:
            #logic for checking for conflicts
            result =1 
            
            
    def printSchedule(self):
        result = self.conn.query("SELECT REGISTEREDCOURSES FROM STUDENTS WHERE EMAIL = '" + self.Email+ "'")
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

    def print_search_roster(self):     #Billy Hingston
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
            print (i[0])
            if testactive:
                    assert str(i[0]) == str(testassert[namecount + 1]), f'X Results do not match. Expected Value: {testassert[count]}. Actual Value: {i[count]}'
                    print('✔ Test Passed!') 
                    namecount += 1        
        search = input("If you would like to search for a specific student, press 1. Otherwise, press 0 to return to the main menu: ") #Regis
        if search == '1':
            student_found = 0
            get_student = input("Please enter the first name of the student you want to search for: ")
            for i in self.roster:
                if i[0] == get_student:
                    student_found = 1
                    print(i[0])
            if student_found == 0:
                print("Student not found!")

   # def SearchCourseRoster(self):
   #    #functionality merged into print_search_roster        
   #   return True

    def print_teaching(self): #Regis
        inst_dept = self.conn.query(f"""SELECT DEPT FROM INSTRUCTOR WHERE ID = {self.ID} """)
        query_result = self.conn.query(f"""SELECT * FROM COURSE WHERE DEPARTMENT = '{inst_dept[0][0]}'""")
        print('Displayed below is your teaching schedule: ')
        for i in query_result:
            print(i)
       
class Admin(User):
    
    def __init__(self, in_name):
        self.sur_name = in_name
        
    def add_course(self):       #Micah
        addCRN = input("Enter the course CRN you want to add: ")
        results = self.conn.query(f"""Select TITLE From COURSE Where CRN = {addCRN} """)
        if (len(results)==0):
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


#Testing Code

DatabaseURI="assignment5.db"
db = sqlite3.connect(DatabaseURI)
cursor = db.cursor()



stud = 0
inst = 0
adm = 0

if testactive ==1:
        #begin unit test
    time.sleep(1)
    keyboard.write(testcase[0])
    keyboard.press('enter')
    print (f"Password Entered: {testcase[0]}")
    ## ---------------- UNIT TEST HERE  ----------------------
passw = input("Enter your password: ")

#STUDENT
cursor.execute("""SELECT NAME from STUDENT where PASSWORD = (SELECT PASSWORD From STUDENT where PASSWORD = '%s'  )""" % (passw))
query_result = cursor.fetchall()
for i in query_result:                          #Billy Hingston
    print("Welcome Student " + str(i[0]))
    if testactive:
        for count, j in enumerate(i):
            assert str(i[count]) == str(testassert[count]), f'X Results do not match. Expected Value: {testassert[count]}. Actual Value: {i[count]}'
            print('✔ Test Passed!') 
    stud = i

# INSTRUCTOR
cursor.execute("""SELECT SURNAME from INSTRUCTOR where PASSWORD = (SELECT PASSWORD From INSTRUCTOR where PASSWORD = '%s'  )""" % (passw))
query_result = cursor.fetchall()
for i in query_result:                          #Billy Hingston
    print("Welcome Instructor " + str(i[0]))
    inst = i
    if testactive:
        for count, j in enumerate(i):
            assert str(i[count]) == str(testassert[count]), f'X Results do not match. Expected Value: {testassert[count]}. Actual Value: {i[count]}'
            print('✔ Test Passed!') 

# ADMIN
cursor.execute("""SELECT SURNAME from ADMIN where PASSWORD = (SELECT PASSWORD From ADMIN where PASSWORD = '%s'  )""" % (passw))
query_result = cursor.fetchall()
for i in query_result:                          #Billy Hingston
    print("Welcome Admin " + str(i[0]))
    if testactive:
        for count, j in enumerate(i):
            assert str(i[count]) == str(testassert[count]), f'X Results do not match. Expected Value: {testassert[count]}. Actual Value: {i[count]}'
            print('✔ Test Passed!') 
    adm = i

select = 1

if testactive:
    for i in range(len(testcase))[1:]:
        keyboard.write(testcase[i])
        keyboard.press('enter')

#keyboard.press_and_release("enter")
if stud != 0 or inst != 0 or adm != 0:  #Billy Hingston
    while select != 0: #Billy Hingston (log out)
        print("-----------------------------\n0) Logout")
        if inst !=0:  # functions for instructor
            user_inst = Instructor(str(inst))
            cursor.execute(f"""SELECT ID FROM INSTRUCTOR WHERE SURNAME = '{inst[0]}'""")#temp query to set ID
            query_result = cursor.fetchall()
            user_inst.ID = query_result[0][0]
            print("1) Assemble and print course roster.")
            print("2) Print teaching schedule")
            print("5) Search all courses")
            print("6) Search courses with a filter")
            select = int(input("Selct an option: "))
            if select == 0:
                print("********** Goodbye! **********")
            elif select == 1:
                user_inst.print_search_roster()    #Billy Hingston
            elif select == 2:
                user_inst.print_teaching() #Regis
            elif select == 5:
                user_inst.search_all()    
            elif select == 6:
                user_inst.search_filter()   
            else:
                print("Invalid Selection")
        elif stud !=0:    # functions for student
            user_stud = Student(str(stud))
            print("5) Search all courses")
            print("6) Search courses with a filter")
            select = input("Selct an option: ")
            select = int(select)
            if select == 0:
                print("********** Goodbye! **********")
            elif select == 5:
                user_stud.search_all()    
            elif select == 6:
                user_stud.search_filter()   
            else:
                print("Invalid Selection")
        elif adm!=0:# functions for admin
           
           
            user_admin = Admin(str(adm))
            print("1) Add a new course")
            print("2) Remove a course")
            print("3) Add a course from a student")
            print("4) Remove a course from a student")
            print("5) Search all courses")
            print("6) Search courses with a filter")
            print("7) Add a new student")
            print("8) Remove a student")
            print("9) Add a new instructor")
            print("10) Remove an instructor")
            select = int(input("Selct an option: "))
            if (select == 0):
                print("********** Goodbye! **********")
            elif select == 1:
                user_admin.add_course()    
            elif select == 2:
                user_admin.remove_course()
            elif select == 3:
                user_admin.add_course_student()    
            elif select == 4:
                user_admin.remove_course_student()
            elif select == 5:
                user_admin.search_all()    
            elif select == 6:
                user_admin.search_filter()
            elif select == 7:
                user_admin.addStudent()
            elif select == 8:
                user_admin.removeStudent()
            elif select == 9:
                user_admin.addInstructor()
            elif select == 10:
                user_admin.removeInstructor()
        else:
            print("Invalid Selection")
else:
    print("Incorrect password")
    
    
    

        
