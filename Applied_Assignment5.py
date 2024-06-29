import sqlite3

# database file connection 
database = sqlite3.connect("assignment5.db") 
  
# cursor objects are used to traverse, search, grab, etc. information from the database, similar to indices or pointers  
cursor = database.cursor() 
class User:
    #def __init__(self, in_name):
    #    self.sur_name = in_name
    def search_all(self):
        print("Entire course table")
        cursor.execute("""SELECT * FROM COURSE""")
        query_result = cursor.fetchall()
        num_fields = len(cursor.description) #get the column names into a list
        field_names = [i[0] for i in cursor.description]
        for i in query_result:
            print(i)	
        
    def print_course(self):
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
        cursor.execute(f"""SELECT * FROM COURSE WHERE {filter} = "{filterval}" """)
        query_result = cursor.fetchall()
        #num_fields = len(cursor.description) #get the column names into a list
        #field_names = [i[0] for i in cursor.description]
        for i in query_result:
            print(i)	
        
class Student(User):
    def __init__(self, in_name):
        self.sur_name = in_name

class Instructor(User):
    def __init__(self, in_name):
        self.roster = []
        self.sur_name = in_name

    def print_roster(self):
        crn = input("To see all students in the course, enter CRN of course: ")
        cursor.execute("""SELECT NAME from STUDENT where CLASS1 =  '%s'  """ % (crn))
        query_result = cursor.fetchall()
        for i in query_result:
            app = i
            self.roster.append(app)
        cursor.execute("""SELECT NAME from STUDENT where CLASS2 =  '%s'  """ % (crn))
        query_result = cursor.fetchall()
        for i in query_result:
            app = i
            self.roster.append(app)
        cursor.execute("""SELECT NAME from STUDENT where CLASS3 =  '%s'  """ % (crn))
        query_result = cursor.fetchall()
        for i in query_result:
            app = i
            self.roster.append(app)
        cursor.execute("""SELECT NAME from STUDENT where CLASS4 =  '%s'  """ % (crn))
        query_result = cursor.fetchall()
        for i in query_result:
            app = i
            self.roster.append(app)
        cursor.execute("""SELECT NAME from STUDENT where CLASS5 =  '%s'  """ % (crn))
        query_result = cursor.fetchall()
        for i in query_result:
            app = i
            self.roster.append(app)
        # print
        for i in self.roster:
            print (i)
class Admin(User):
    def __init__(self, in_name):
        self.sur_name = in_name
    def add_course(self):
        addCRN = input("Enter the course CRN you want to add: ")
        cursor.execute(f"""Select TITLE From COURSE Where CRN = {addCRN} """)
        query_result = cursor.fetchall()
        if (len(query_result) == 0):
            addTitle= input("Enter the title: ")
            addDep= input("Enter the department: ")
            addTime= input("Enter the time: ")
            addDOW= input("Enter the DOW: ")
            addSem= input("Enter the semester: ")
            addYear= input("Enter the year: ")
            addCred =input("Enter the amount of credits: ")
            cursor.execute(f"""INSERT INTO COURSE VALUES({addCRN}, '{addTitle}','{addDep}', {addTime}, '{addDOW}', '{addSem}', {addYear}, {addCred})""")
            database.commit() 
        else:
            print("Course already has that CRN")

    def remove_course(self):
        removeCRN= input("Enter the course CRN you want to remove: ")
        
        cursor.execute(f"""Select TITLE From COURSE Where CRN = {removeCRN} """)
        query_result = cursor.fetchall()
        if (len(query_result) == 0):
            print("A course with that CRN does not exist")
        else:
            cursor.execute(f"""DELETE FROM COURSE WHERE CRN = {removeCRN}""")
            database.commit() 
    def remove_course_student(self):
        stuID=input("Please enter a students ID: ")
        cursor.execute(f"""Select CLASS1,CLASS2,CLASS3,CLASS4,CLASS5 From STUDENT Where ID = {stuID} """)
        query_result = cursor.fetchall()
        for i in query_result:
            print("The courses being taken are:")
            print(i)
        removeclass =input("Which course do you want to remove?")
        cursor.execute(f"UPDATE STUDENT SET CLASS1 = NULL WHERE CLASS1 = {removeclass} AND ID = {stuID}")
        cursor.execute(f"UPDATE STUDENT SET CLASS2 = NULL WHERE CLASS2 = {removeclass} AND ID = {stuID}")
        cursor.execute(f"UPDATE STUDENT SET CLASS3 = NULL WHERE CLASS3 = {removeclass} AND ID = {stuID}")
        cursor.execute(f"UPDATE STUDENT SET CLASS4 = NULL WHERE CLASS4 = {removeclass} AND ID = {stuID}")
        cursor.execute(f"UPDATE STUDENT SET CLASS5 = NULL WHERE CLASS5 = {removeclass} AND ID = {stuID}")
        database.commit() 




    def add_course_student(self):
        stuID=input("Please enter a students ID: ")
        ClassAdd=input("Enter the course CRN you want to add: ")
        cursor.execute(f"""Select CLASS1,CLASS2,CLASS3,CLASS4,CLASS5 From STUDENT Where ID = {stuID} """)
        query_result = cursor.fetchone()
        if query_result is not None:
            classes = ['CLASS1', 'CLASS2', 'CLASS3', 'CLASS4', 'CLASS5']
            nextClass = None

            for i in range(len(query_result)):
                if query_result[i] is None:
                    nextClass = classes[i]
                    break

            if nextClass:
                cursor.execute(f"""UPDATE STUDENT SET {nextClass} = {ClassAdd} WHERE ID = {stuID}""")
                database.commit()
                print(f"Course {ClassAdd} added to {nextClass} for student ID {stuID}.")
            else:
                print("No available slot to add the new class.")
        else:
            print(f"No student found with ID {stuID}.")



stud = 0
inst = 0
adm = 0
passw = input("Enter your password: ")

#STUDENT
cursor.execute("""SELECT NAME from STUDENT where PASSWORD = (SELECT PASSWORD From STUDENT where PASSWORD = '%s'  )""" % (passw))
query_result = cursor.fetchall()
for i in query_result:
    print("Welcome Student " + str(i))
    stud = i

# INSTRUCTOR
cursor.execute("""SELECT SURNAME from INSTRUCTOR where PASSWORD = (SELECT PASSWORD From INSTRUCTOR where PASSWORD = '%s'  )""" % (passw))
query_result = cursor.fetchall()
for i in query_result:
    ("Welcome Instructor " + str(i))
    inst = i

# ADMIN
cursor.execute("""SELECT SURNAME from ADMIN where PASSWORD = (SELECT PASSWORD From ADMIN where PASSWORD = '%s'  )""" % (passw))
query_result = cursor.fetchall()
for i in query_result:
    print("Welcome Admin " + str(i))
    adm = i

select = 1
if stud != 0 or inst != 0 or adm != 0:
    while select != 0:
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
                user_inst.print_roster()
            elif select == 5:
                user_inst.search_all()    
            elif select == 6:
                user_inst.print_course()   
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
                user_stud.print_course()   
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
                user_admin.print_course()
        else:
            print("Invalid Selection")
else:
    print("Incorrect password")