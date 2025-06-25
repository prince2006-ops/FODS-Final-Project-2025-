import os
import pandas as pd
#main class to run the system
class System_management:
    def __init__(self):
        self.users={}
        self.eca={}
        self.grades={}
        self.password={}
        self.load_files()
# Adding the userdata from the files.
    def load_files(self):
        try:
            if os.path.exists("user.txt"):
                with open('user.txt','r') as f:
                    for line in f:
                        user_id,name,role,contact=line.strip().split(",")
                        self.users[user_id]={
                            "name":name,
                            "role":role,
                            "contact":contact
                            }
            if os.path.exists('password.txt'):
                with open('password.txt', 'r') as f:
                    for line in f:
                        user_id,password=line.strip().split(",")
                        self.password[user_id] = password

            if os.path.exists('grades.txt'):
                with open('grades.txt','r')as f:
                    for line in f:
                        marks=line.strip().split(",")
                        user_id=marks[0]
                        grades=list(map(int,marks[1:]))
                        self.grades[user_id]=grades
            if os.path.exists('eca.txt'):
                with open('eca.txt','r')as f:
                    for line in f:
                        eca=line.strip().split(',')
                        user_id=eca[0]
                        activities=eca[1:]
                        self.eca[user_id]=activities
        except Exception as e:
            print(f"You have {e} exception")
#setting up the login system
    def login(self):
        print("-----Login Page-----")
        while True:
            u_id=input("Enter the id:").strip()
            password=input("Enter the password:").strip()
            if u_id in self.password and self.password[u_id]==password:
                detail=self.users[u_id]
                if detail["role"]=="admin":
                    return Admin(u_id, detail["name"], detail["role"], detail["contact"])
                else:
                    return Student(u_id, detail["name"], detail["role"], detail["contact"])
            else:
                print("Invalid details")
# adding user data in all the txt files
    def append_user(self, user_id, name, role, contact):
        with open("user.txt", "a") as f:
            f.write(f"{user_id},{name},{role},{contact}\n")
        self.users[user_id] = {"name": name, "role": role, "contact": contact}
    def append_password(self, user_id, password):
        with open("password.txt", "a") as f:
            f.write(f"{user_id},{password}\n")
        self.password[user_id] = password
    def append_grades(self, user_id, grades):
        with open("grades.txt", "a") as f:
            f.write(f"{user_id}," + ",".join(map(str, grades)) + "\n")
        self.grades[user_id] = grades
    def append_eca(self, user_id, activities):
        with open("eca.txt", "a") as f:
            f.write(f"{user_id}," + ",".join(activities) + "\n")
        self.eca[user_id] = activities
#used in deleting the user details
    def save_all(self):
        with open("user.txt", "w") as f:
            for uid, value in self.users.items():
                f.write(f"{uid},{value['name']},{value['role']},{value['contact']}\n")
        with open("password.txt", "w") as f:
            for uid, pwd in self.password.items():
                f.write(f"{uid},{pwd}\n")
        with open("grades.txt", "w") as f:
            for uid, grades in self.grades.items():
                f.write(f"{uid}," + ",".join(map(str, grades)) + "\n")
        with open("eca.txt", "w") as f:
            for uid, eca in self.eca.items():
                f.write(f"{uid}," + ",".join(eca) + "\n")

    def run(self):
        user = self.login()
        while True:
            user.menu()  # Step 2: display menu for that user
            choice = input("Choose option: ").strip()  # Step 3: get choice
            # Step 4: match choice to functionality
            if user.role == "admin":
                if choice == "1":
                    user.add_user(self)
                elif choice == "2":
                    print("Update user - To be implemented")
                elif choice == "3":
                    print("Delete user - To be implemented")
                elif choice == "4":
                    print("View users - To be implemented")
                elif choice == "5":
                    print("Logging out...")
                    break
            else:
                if choice == "1":
                    print("View profile - To be implemented")
                elif choice == "2":
                    print("View grades - To be implemented")
                elif choice == "3":
                    print("View ECA - To be implemented")
                elif choice == "4":
                    print("Logging out...")
                    break

class User:
    def __init__(self,user_id,name,role,phone):
        self.user_id=user_id
        self.name=name
        self.role=role
        self.contact=phone
        def menu(self):
            pass

class Admin(User):
    def menu(self):
        print("1. Add user")
        print("2. Update user")
        print("3. Delete user")
        print("4. Generate insights")
        print("5. Logout")

    def add_user(self, system):
        print("----- Add New User -----\n")
        user_id = input("User ID: ").strip()
        if user_id in system.users:
            print("User already exists.")
            return

        name = input("Name: ").strip()
        role = input("Role : ").strip().lower()
        if role not in ("admin", "student"):
            print("Role must be 'admin' or 'student'.")
            return

        contact = input("Contact: ").strip()
        password = input("Password: ").strip()

        if role=='student':
            grades_input = input("Enter grades separated by commas (e.g., 85,90,78): ").strip()
            grades = [int(g.strip()) for g in grades_input.split(",") if g.strip().isdigit()]
            eca_input = input("Enter ECA activities separated by commas (e.g., football,robotics): ").strip()
            activities = [e.strip() for e in eca_input.split(",") if e.strip()]
        system.append_user(user_id, name, role, contact)
        system.append_password(user_id, password)
        system.append_grades(user_id, grades)
        system.append_eca(user_id, activities)


class Student(User):
    def menu(self):
        print("1.View Profile")
        print("2.View Grades")
        print("3.View ECA")
        print("4.Sign out")

if __name__ == "__main__":
    system = System_management()
    system.run()
