import sqlite3
from prettytable import PrettyTable
# database file connection 
database = sqlite3.connect("assignment3.db") 
  
# cursor objects are used to traverse, search, grab, etc. information from the database, similar to indices or pointers  
cursor = database.cursor() 
  
# SQL command to create a table in the database 
sql_command = """CREATE TABLE COURSE (  
CRN INTEGER PRIMARY KEY NOT NULL,
TITLE TEXT NOT NULL,
DEPARTMENT TEXT NOT NULL,
TIME INTEGER NOT NULL,
DOW TEXT NOT NULL,
SEMESTER TEXT NOT NULL,
YEAR INTEGER NOT NULL,
CREDITS INTEGER NOT NULL)
;"""
  
# execute the statement 
cursor.execute(sql_command) 
 
# SQL command to insert the data in the table, must be done one at a time 
sql_command = """INSERT INTO STUDENT VALUES(10011, 'Cole', 'Hill', 2025, 'BSCO', 'hcole');"""
cursor.execute(sql_command) 

sql_command = """INSERT INTO STUDENT VALUES(10012, 'Joe', 'Knight', 2024, 'BSEE', 'kjoe');"""
cursor.execute(sql_command) 

sql_command = """DELETE FROM INSTRUCTOR WHERE ID = 20001"""
cursor.execute(sql_command) 

sql_command = """UPDATE ADMIN SET TITLE = 'Vice-President' WHERE ID = 30002"""
cursor.execute(sql_command) 

sql_command = """INSERT INTO COURSE VALUES(3225, 'Applied Programming Concepts', 'BSCO', 8, 'TRTH', 'Summer', 2024, 4)"""
cursor.execute(sql_command)

sql_command = """INSERT INTO COURSE VALUES(3226, 'BSEE Class', 'BSEE', 9, 'MW', 'Spring', 2024, 4)"""
cursor.execute(sql_command)

sql_command = """INSERT INTO COURSE VALUES(3227, 'HUSS Class', 'HUSS', 12, 'TRTHF', 'Fall', 2025, 4)"""
cursor.execute(sql_command)

sql_command = """INSERT INTO COURSE VALUES(3228, 'BCOS Class', 'BCOS', 15, 'MTH', 'Spring', 2024, 4)"""
cursor.execute(sql_command)

sql_command = """INSERT INTO COURSE VALUES(3229, 'BSME Class', 'BSME', 15, 'TRF', 'Summer', 2024, 3)"""
cursor.execute(sql_command)

# # QUERY FOR PROFESSORS
print("Professors that host BSCO Classes:")
cursor.execute("""Select name || ' ' || surname From Instructor Where dept = (Select department From Course where DEPARTMENT = "BSCO"  )""")
query_result = cursor.fetchall()
for i in query_result:
	print(i)

print("Professors that host BSEE Classes:")
cursor.execute("""Select name || ' ' || surname From Instructor Where dept = (Select department From Course where DEPARTMENT = "BSEE"  )""")
query_result = cursor.fetchall()
for i in query_result:
	print(i)

print("Professors that host HUSS Classes:")
cursor.execute("""Select name || ' ' || surname From Instructor Where dept = (Select department From Course where DEPARTMENT = "HUSS"  )""")
query_result = cursor.fetchall()
for i in query_result:
	print(i)

print("Professors that host BCOS Classes:")
cursor.execute("""Select name || ' ' || surname From Instructor Where dept = (Select department From Course where DEPARTMENT = "BCOS"  )""")
query_result = cursor.fetchall()
for i in query_result:
	print(i)

print("Professors that host BSME Classes:")
cursor.execute("""Select name || ' ' || surname From Instructor Where dept = (Select department From Course where DEPARTMENT = "BSME"  )""")
query_result = cursor.fetchall()
for i in query_result:
	print(i)			


print("Entire student table")
cursor.execute("""SELECT * FROM STUDENT""")
query_result = cursor.fetchall()
num_fields = len(cursor.description) #get the column names into a list
field_names = [i[0] for i in cursor.description]

myTable1 = PrettyTable(field_names)
for i in query_result:
	myTable1.add_row(i)
print(myTable1)	

print("Entire instructor table")
cursor.execute("""SELECT * FROM INSTRUCTOR""")
query_result = cursor.fetchall()
num_fields = len(cursor.description) #get the column names into a list
field_names = [i[0] for i in cursor.description]

myTable2 = PrettyTable(field_names)
for i in query_result:
	myTable2.add_row(i)
print(myTable2)	

print("Entire admin table")
cursor.execute("""SELECT * FROM ADMIN""")
query_result = cursor.fetchall()
num_fields = len(cursor.description) #get the column names into a list
field_names = [i[0] for i in cursor.description]

myTable3 = PrettyTable(field_names)
for i in query_result:
	myTable3.add_row(i)
print(myTable3)	

print("Entire course table")
cursor.execute("""SELECT * FROM COURSE""")
query_result = cursor.fetchall()
num_fields = len(cursor.description) #get the column names into a list
field_names = [i[0] for i in cursor.description]

myTable4 = PrettyTable(field_names)
for i in query_result:
	myTable4.add_row(i)
print(myTable4)	


print('Testing the course table')
print("Searching for Summer courses:")
cursor.execute("""Select TITLE, CRN, DOW as "DAYS OF THE WEEK", CREDITS, TIME From Course Where SEMESTER = "Summer" """)
query_result = cursor.fetchall()
num_fields = len(cursor.description) #get the column names into a list
field_names = [i[0] for i in cursor.description]

myTable5 = PrettyTable(field_names)
for i in query_result:
	myTable5.add_row(i)
print(myTable5)	

print("Searching for Spring courses available in 2024:")
cursor.execute("""Select TITLE, CRN, DOW as "DAYS OF THE WEEK", CREDITS, TIME From Course Where YEAR = "2024" AND SEMESTER = "Spring" """)
query_result = cursor.fetchall()
num_fields = len(cursor.description) #get the column names into a list
field_names = [i[0] for i in cursor.description]

myTable6 = PrettyTable(field_names)
for i in query_result:
	myTable6.add_row(i)
print(myTable6)	

# To save the changes in the files. Never skip this.  
# If we skip this, nothing will be saved in the database. 
database.commit() 
  
# close the connection 
database.close() 