import sqlite3
from datetime import datetime

#Jared
class dbConnection:
    
    DatabaseURI="assignment5.db"
    cur=None
    db=None
    
    def __init__(self):
        self.db = sqlite3.connect(self.DatabaseURI);
        self.cur = self.db.cursor()
        
    def query(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def queryExecute(self, query):
        self.cur.execute(query)
        self.db.commit()
    

class User:

    #User Class Attributes
    Email=None
    Name=None
    Surname=None
    ID=None
    
    #SQL Database Access Objects
    conn = dbConnection()
           
    
    #def __init__(self, in_name):
    #    self.sur_name = in_name
    def search_all(self): #Regis
        print("Entire course table")
        query_result = self.conn.query("""SELECT * FROM COURSE""") 
        for i in query_result:
            print(i)	
        
    def filter_course(self):#Regis
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
        query_result = self.conn.query(f"SELECT * FROM COURSE WHERE {filter} = {filterval}")
        for i in query_result:
            print(i)	
        
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

    def print_roster(self):     #Billy Hingston
        crn = input("To see all students in the course, enter CRN of course: ")
        for CRN in self.LinkedCourses:
            if (CRN == crn):
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
                for i in self.roster:
                    print (i)
                    
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
            addTitle= input("Enter the title: ")
            addDep= input("Enter the department: ")
            addTime= input("Enter the time: ")
            addDOW= input("Enter the DOW: ")
            addSem= input("Enter the semester: ")
            addYear= input("Enter the year: ")
            addCred =input("Enter the amount of credits: ")
            self.conn.queryExecute(f"""INSERT INTO COURSE VALUES({addCRN}, '{addTitle}','{addDep}', {addTime}, '{addDOW}', '{addSem}', {addYear}, {addCred})""") 
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
            else:
                print("No available slot to add the new class.")
        else:
            print(f"No student found with ID {stuID}.")
            
            #Jared
    def addStudent(self):
        id = input("Please Enter new student ID")
        name = input("Enter Name")
        surname = input("Enter surname")
        email = surname + name[0] + "@wit.edu"
        #logic to check that email is still available
        gradYear = datetime.now().year + 4
        major = input("Please enter major")
        self.conn.queryExecute(f"INSERT INTO STUDENT ({id}, {name}, {surname}, {gradYear}, {major}, {email})")

    #Jared
    def removeStudent(self):
        id = input("Please Enter id of Student you wish to remove")
        result  = self.conn.query(f"SELECT * FROM STUDENT WHERE ID = {id}")
        if result is not None:
            self.conn.queryExecute(f"DELETE FROM STUDENT WHERE ID = {id}")
        else :
            print("This student is not within the database")

    #Jared
    def addInstructor(self):
        id = input("Please Enter new instrutor ID")
        name = input("Enter Name")
        surname = input("Enter surname")
        email = surname + name[0] + "@wit.edu"
        title = input("Enter Instrutor's title")
        dept = input("Enter instrutor's Department")
        #logic to check that email is still available
        hireYear = datetime.now().year
        major = input("Please enter major")
        self.conn.queryExecute(f"INSERT INTO STUDENT ({id}, {name}, {surname}, {title}, {major}, {hireYear}, {dept}, {email})")

    #Jared
    def removeInstructor(self):
        id = input("Please Enter id of Instrutor you wish to remove")
        result  = self.conn.query(f"SELECT * FROM INSTRUTOR WHERE ID = {id}")
        if result is not None:
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
passw = input("Enter your password: ")

#STUDENT
cursor.execute("""SELECT NAME from STUDENT where PASSWORD = (SELECT PASSWORD From STUDENT where PASSWORD = '%s'  )""" % (passw))
query_result = cursor.fetchall()
for i in query_result:                          #Billy Hingston
    print("Welcome Student " + str(i))
    stud = i

# INSTRUCTOR
cursor.execute("""SELECT SURNAME from INSTRUCTOR where PASSWORD = (SELECT PASSWORD From INSTRUCTOR where PASSWORD = '%s'  )""" % (passw))
query_result = cursor.fetchall()
for i in query_result:                          #Billy Hingston
    ("Welcome Instructor " + str(i))
    inst = i

# ADMIN
cursor.execute("""SELECT SURNAME from ADMIN where PASSWORD = (SELECT PASSWORD From ADMIN where PASSWORD = '%s'  )""" % (passw))
query_result = cursor.fetchall()
for i in query_result:                          #Billy Hingston
    print("Welcome Admin " + str(i))
    adm = i

select = 1
if stud != 0 or inst != 0 or adm != 0:  #Billy Hingston
    while select != 0: #Billy Hingston (log out)
        print("-----------------------------\n0) Exit")
        if inst !=0:  # functions for instructor
            user_inst = Instructor(str(inst))
            print("1) Assemble and print course roster.")
            print("5) Search all courses")
            print("6) Search courses with a filter")
            select = int(input("Selct an option: "))
            if select == 0:
                print("********** Goodbye! **********")
            elif select == 1:
                user_inst.print_roster()    #Billy Hingston
            elif select == 5:
                user_inst.search_all()    
            elif select == 6:
                user_inst.filter_course()   
            else:
                print("Invalid Selection")
        elif stud !=0:    # functions for student
            user_stud = Student(str(stud))
            print("5) Search all courses")
            print("6) Search courses with a filter")
            select = int(input("Selct an option: "))
            if select == 0:
                print("********** Goodbye! **********")
            elif select == 5:
                user_stud.search_all()    
            elif select == 6:
                user_stud.filter_course()   
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
                user_admin.filter_course()
        else:
            print("Invalid Selection")
else:
    print("Incorrect password")
    
    
    
