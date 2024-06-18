import class1

s1 = class1.Student("John", "Doe", 67)
t1 = class1.Instructor("Mary", "Smith", 23)
a1 = class1.Admin("Henry", "Wentworth", 2)
while True:
    user_in = int(input("\nWelcome to Leapord Web!\nEnter 1 for Student\nEnter 2 for Teacher\nEnter 3 for Admin\nEnter 4 to Exit\n"))
    match user_in:
        case 1:
            s1.print_all()
            s1.search_course()
            s1.add_course()
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
        case _:
            print("Enter a valid input\n")