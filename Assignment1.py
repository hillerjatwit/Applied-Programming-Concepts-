import class1
import sqlite3
#from prettytable import PrettyTable
# database file connection 
database = sqlite3.connect("assignment3.db") 
   
s1 = class1.Student("John", "Doe", 67)
t1 = class1.Instructor("Mary", "Smith", 23)
a1 = class1.Admin("Henry", "Wentworth", 2)
while True:
    user_in = int(input("\nWelcome to Leapord Web!\nEnter 1 for Student\nEnter 2 for Teacher\nEnter 3 for Admin\nEnter 4 to Exit\n"))
    match user_in:
        case 1:
            s1.print_all()
            s1.search_all()

            s1.add_course(3226)
            s1.drop_course()
            s1.print_schedule() 
        case 2:
            t1.print_all()
            t1.print_schedule()
            t1.print_classlist()
            t1.search_course()
        case 3:
            a1.print_all()
            a1.add_course()
            a1.drop_course()
            a1.add_user()
            a1.remove_user()
            a1.add_student()
            a1.drop_student()
            a1.search_roster()
            a1.print_roster()
            a1.search_courses()
            a1.print_courses()
        case 4:
            print("You have exited the program.\n")
            break
        case 5:
            print("You have entered debug mode\n")
            user_in = int(input("\nEnter a function to test\n1) Search all courses \n2) Search for course with a filter\n"))
            match user_in:
                case 1:
                    s1.search_all()
                    break
                case 2:
                    user_in = int(input("\nEnter a coulumn to filter courses by\n1) CRN\n2) Title\n3) Department\n4) Time\n5) Day of the Week\n6) Year\n7) Credits\n"))
                    user_in2 = str(input("\nEnter the value to filter: "))
                    match user_in:
                        case 1:
                            user_in3 = "CRN"
                        case 2:
                            user_in3 = "TITLE"
                        case 3:
                            user_in3 = "DEPARTMENT"
                        case 4:
                            user_in3 = "TIME"
                        case 5:
                            user_in3 = "DOW"
                        case 6:
                            user_in3 = "SEMESTER"
                        case 7:
                            user_in3 = "CREDITS"
                        case _:
                            user_in3 = "CRN" #default to CRN if invalid input entered
                            print("Invalid input entered, defaulting to CRN\n")

                    s1.print_course(user_in3, user_in2)
                    break
            
            break
        case _:
            print("Enter a valid input\n")