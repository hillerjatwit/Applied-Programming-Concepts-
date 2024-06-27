import sqlite3

# database file connection 
database = sqlite3.connect("assignment5.db") 
  
# cursor objects are used to traverse, search, grab, etc. information from the database, similar to indices or pointers  
cursor = database.cursor() 

class Instructor:
    def __init__(self, in_name):
        self.sur_name = in_name
        self.roster = []
		
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
	print("Welcome Instructor " + str(i))
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
			select = int(input("Selct an option: "))
			if select == 1:
				user_inst.print_roster()
			elif select == 0:
				print("********** Goodbye! **********")
			else:
				print("Invalid Selection")
		elif stud !=0:    # functions for student
			select = int(input("Selct an option: "))
			if select == 0:
				print("********** Goodbye! **********")
			else:
				print("Invalid Selection")
		else:           # functions for admin
			select = int(input("Selct an option: "))
			if select == 0:
				print("********** Goodbye! **********")
			else:
				print("Invalid Selection")
else:
	print("Incorrect password")