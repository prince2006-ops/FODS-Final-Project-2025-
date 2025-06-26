import os
import pandas as pd

# Main class to run the system
class System_management:
    def __init__(self):
        self.users = {}
        self.eca = {}
        self.grades = {}
        self.password = {}
        self.load_files()

    # Adding the userdata from the files.
    def load_files(self):
        try:
            if os.path.exists("user.txt"):
                with open('user.txt', 'r') as f:
                    for line in f:
                        user_id, name, role, contact = line.strip().split(",")
                        self.users[user_id] = {
                            "name": name,
                            "role": role,
                            "contact": contact
                        }
            if os.path.exists('password.txt'):
                with open('password.txt', 'r') as f:
                    for line in f:
                        user_id, password = line.strip().split(",")
                        self.password[user_id] = password

            if os.path.exists('grades.txt'):
                with open('grades.txt', 'r') as f:
                    next(f)  # Skip header
                    for line in f:
                        marks = line.strip().split(",")
                        user_id = marks[0]
                        grades = list(map(int, marks[1:]))
                        self.grades[user_id] = grades
            if os.path.exists('eca.txt'):
                with open('eca.txt', 'r') as f:
                    for line in f:
                        eca = line.strip().split(',')
                        user_id = eca[0]
                        activities = eca[1:]
                        self.eca[user_id] = activities
        except Exception as e:
            print(f"You have {e} exception")

    # setting up the login system
    def login(self):
        print("-----Login Page-----")
        while True:
            u_id = input("Enter the id:").strip()
            password = input("Enter the password:").strip()
            if u_id in self.password and self.password[u_id] == password:
                detail = self.users[u_id]
                if detail["role"] == "admin":
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

    # deleting user info by user id
    def delete_user(self, user_id):
        if user_id in self.users:
            self.users.pop(user_id)
            self.password.pop(user_id, None)
            self.grades.pop(user_id, None)
            self.eca.pop(user_id, None)
            self.save_all()
            print(f" User '{user_id}' deleted successfully.")
        else:
            print(" User not found.")

    # used in deleting the user details
    def save_all(self):
        with open("user.txt", "w") as f:
            for uid, value in self.users.items():
                f.write(f"{uid},{value['name']},{value['role']},{value['contact']}\n")
        with open("password.txt", "w") as f:
            for uid, pwd in self.password.items():
                f.write(f"{uid},{pwd}\n")
        with open("grades.txt", "w") as f:
            # Write header for grades file
            f.write("user_id,FOM,FODS,IT,English,ITF\n")
            for uid, grades in self.grades.items():
                f.write(f"{uid}," + ",".join(map(str, grades)) + "\n")
        with open("eca.txt", "w") as f:
            for uid, eca in self.eca.items():
                f.write(f"{uid}," + ",".join(eca) + "\n")

    # Viewing users with options for specific or all, and category selection
    def view_users(self):
        print("\n1. User's info")
        print("2. Grades")
        print("3. ECA")
        choice = input("Choose the number to view (1-3): ").strip()

        if choice not in ('1', '2', '3'):
            print("Invalid category choice!\n")
            return

        print("\nChoose the option:")
        print("1. Specific user")
        print("2. All users")
        option_choice = input("Enter your choice (1 or 2): ").strip()

        if option_choice == '1':
            user_id = input("Enter the user ID: ").strip()

            if user_id not in self.users:
                print("User ID not found!\n")
                return

            if choice == '1':  # Basic info
                u = self.users[user_id]
                print(f"\n--- USER INFO ---")
                print(f"ID      : {user_id}")
                print(f"Name    : {u['name']}")
                print(f"Role    : {u['role']}")
                print(f"Contact : {u['contact']}\n")

            elif choice == '2':  # Grades
                print("\n--- GRADES ---")
                try:
                    grade = self.grades[user_id]
                    print("FOM,FODS,IT,English,ITF")
                    print(grade)
                except KeyError:
                    print("No grades on file.")
                print()

            elif choice == '3':  # ECA
                print("\n--- ECA ---")
                try:
                    eca = self.eca[user_id]
                    print(eca)
                except KeyError:
                    print("No ECA activities on file.")
                print()

        elif option_choice == '2':
            if choice == '1':
                print("\n--- USERS LIST ---")
                for uid, value in self.users.items():
                    print(f"ID: {uid}")
                    print(f"Name: {value['name']}")
                    print(f"Role: {value['role']}")
                    print(f"Contact: {value['contact']}\n")

            elif choice == '2':
                print("\n--- GRADES LIST ---")
                print("ID-FOM,FODS,IT,English,ITF")
                for uid, marks in self.grades.items():
                    print(f"{uid} - {marks}")
                print()

            elif choice == '3':
                print("\n--- ECA LIST ---")
                for uid, activities in self.eca.items():
                    print(f"ID: {uid} - ECA: {activities}")
                print()

        else:
            print("Invalid option choice!\n")

    def run(self):
        user = self.login()
        while True:
            user.menu()  # display menu for that user
            choice = input("Choose option: ").strip()
            if user.role == "admin":
                if choice == "1":
                    user.add_user(self)
                elif choice == "2":
                    user.delete_user(self)
                elif choice == "3":
                    user.view_users(self)
                elif choice == "4":
                    print("Logging out...")
                    break
                else:
                    print("Invalid option. Try again.")
            else:
                if choice == "1":
                    user.view_profile(self)
                elif choice == "2":
                    user.view_grades(self)
                elif choice == "3":
                    user.view_eca(self)
                elif choice == "4":
                    print("Logging out...")
                    break
                else:
                    print("Invalid option. Try again.")

#main class
class User:
    def __init__(self, user_id, name, role, phone):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.contact = phone

    def menu(self):
        pass


class Admin(User):
    def menu(self):
        print("\n1. Add user")
        print("2. Delete user")
        print("3. View Users")
        print("4. Logout")

    def add_user(self, system):
        print("----- Add New User -----\n")
        user_id = input("User ID: ").strip()
        if user_id in system.users:
            print("User already exists.")
            return

        name = input("Name: ").strip()
        role = input("Role : ").strip().lower()
        if role not in ("admin", "student"):
            print("Invalid Role!!! Only accepts admin or student")
            return

        contact = input("Contact: ").strip()
        password = input("Password: ").strip()

        system.append_user(user_id, name, role, contact)
        system.append_password(user_id, password)

        if role == 'student':
            grades_input = input("Enter grades : ").strip()
            grades = []
            for g in grades_input.split(","):
                if g.strip().isdigit():
                    grades.append(int(g.strip()))
            eca_input = input("Enter ECA : ").strip()
            activities = []
            for e in eca_input.split(","):
                value = e.strip()
                if value:
                    activities.append(value)

            system.append_grades(user_id, grades)
            system.append_eca(user_id, activities)

    def delete_user(self, system):
        user_id = input("Enter the user id:").strip()
        system.delete_user(user_id)

    def view_users(self, system):
        system.view_users()


class Student(User):
    def menu(self):
        print("\n1.View Profile")
        print("2.View Grades")
        print("3.View ECA")
        print("4.Sign out")
    def view_profile(self,system):
        self_info=system.users[self.user_id]
        print("**** Your Details ****")
        print("\n--- MY PROFILE ---")
        print(f"ID      : {self.user_id}")
        print(f"Name    : {self_info['name']}")
        print(f"Role    : {self_info['role']}")
        print(f"Contact : {self_info['contact']}\n")

    def view_grades(self, system):
        print("\n--- MY GRADES ---")
        try:
            print("FOM,FODS,IT,English,ITF")
            g = system.grades[self.user_id]
            print(g)
        except KeyError:
            print("No grades on file.")
        print()

    def view_eca(self, system):
        print("\n--- MY ECA ---")
        try:
            e = system.eca[self.user_id]
            print(e)
        except KeyError:
            print("No ECA activities on file.")
        print()


if __name__ == "__main__":
    system = System_management()
    system.run()
