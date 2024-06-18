class User:
    def __init__(self, first_name, last_name, ID):
        self.first_name = first_name
        self.last_name = last_name
        self.ID = ID
    
    def set_firstname(self):
        self.first_name = input("Enter the first name of the User: ")
    def set_lastname(self):
        self.last_name = input("Enter the User's last name: ")
    def set_ID(self):
        self.ID =  input("Enter the User's ID: ")
    def print_all(self):
        print("The User's name is " + self.first_name + " " + self.last_name + ", who has an ID of: " + str(self.ID))

class Student(User):
    def search_course(self):
        print("Search course function successfully run!")
    def add_course(self):
        print("Add course function successfully run!")
    def drop_course(self):
        print("Drop course function successfully run!")
    def print_schedule(self):
        print("Print schedule function successfully run!")

class Instructor(User):
    def print_schedule(self):
        print("Print schedule function successfully run!")
    def print_classlist(self):
        print("Print class list function successfully run!")
    def search_course(self):
        print("Search course function successfully run!")

class Admin(User):
    def add_course(self):
        print("Add course function successfully run!")
    def drop_course(self):
        print("Drop course function successfully run!")
    def add_user(self):
        print("Add user function successfully run!")
    def remove_user(self):
        print("Remove user function successfully run!")
    def add_student(self):
        print("Add student to course function successfully run!")
    def drop_student(self):
        print("Remove student from course function successfully run!")
    def search_roster(self):
        print("Search roster function successfully run!")
    def print_roster(self):
        print("Print roster function successfully run!")
    def search_courses(self):
        print("Search courses function successfully run!")
    def print_courses(self):
        print("Print courses function successfully run!")