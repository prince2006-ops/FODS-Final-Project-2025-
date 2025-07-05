# importing necessary library
import os
import pandas as pd
import matplotlib.pyplot as plt

# Main class to run the system
class System_management:
    def __init__(self):
        self.users = {}
        self.eca = {}
        self.grades = {}
        self.password = {}
        self.load_files()
#loading all the data from the txt file.
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
                    next(f)
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
# Validates the login and returns the class accordingly
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
# helps to append the file when admin adds users.
    # appends user info
    def append_user(self, user_id, name, role, contact):
        with open("user.txt", "a") as f:
            f.write(f"{user_id},{name},{role},{contact}\n")
        self.users[user_id] = {"name": name, "role": role, "contact": contact}
    # appends user password
    def append_password(self, user_id, password):
        with open("password.txt", "a") as f:
            f.write(f"{user_id},{password}\n")
        self.password[user_id] = password
    # appends user grades
    def append_grades(self, user_id, grades):
        with open("grades.txt", "a") as f:
            f.write(f"{user_id}," + ",".join(map(str, grades)) + "\n")
        self.grades[user_id] = grades
    # appends user eca
    def append_eca(self, user_id, activities):
        with open("eca.txt", "a") as f:
            f.write(f"{user_id}," + ",".join(activities) + "\n")
        self.eca[user_id] = activities
# deletes the data of the file.
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
#saves the data  in file after updating and deleting from the file.
    def save_all(self):
        with open("user.txt", "w") as f:
            for uid, value in self.users.items():
                f.write(f"{uid},{value['name']},{value['role']},{value['contact']}\n")
        with open("password.txt", "w") as f:
            for uid, pwd in self.password.items():
                f.write(f"{uid},{pwd}\n")
        with open("grades.txt", "w") as f:
            f.write("user_id,FOM,FODS,IT,English,ITF\n")
            for uid, grades in self.grades.items():
                f.write(f"{uid}," + ",".join(map(str, grades)) + "\n")
        with open("eca.txt", "w") as f:
            for uid, eca in self.eca.items():
                f.write(f"{uid}," + ",".join(eca) + "\n")
# function to view users to admin.
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

            if choice == '1':
                u = self.users[user_id]
                print(f"\n--- USER INFO ---")
                print(f"ID      : {user_id}")
                print(f"Name    : {u['name']}")
                print(f"Role    : {u['role']}")
                print(f"Contact : {u['contact']}\n")

            elif choice == '2':
                print("\n--- GRADES ---")
                try:
                    grade = self.grades[user_id]
                    print("FOM,FODS,IT,English,ITF")
                    print(grade)
                except KeyError:
                    print("No grades on file.")
                print()

            elif choice == '3':
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
# provides data insights to admin.
    def data_insights(self):
        print("Why do you want to view?")
        print("1.Grade trends")
        print('2. ECA records')
        print('3. Performance alerts')
        choice = input("Choose any option:")

        if choice == '1':
            subjects = ["FOM", "FODS", "IT", "English", "ITF"]
            try:
                df = pd.DataFrame.from_dict(self.grades, orient='index', columns=subjects)
            except ValueError:
                print("Incomplete data")
                return
            avg = df.mean().round(1)
            print(avg.to_string())
            plt.figure(figsize=(7, 4))
            avg.plot(kind='bar', color='lightgreen')
            plt.title('Average grades per Subject')
            plt.ylabel("Marks")
            plt.xlabel("Subjects")
            plt.show()

        elif choice == '2':
            eca_counts = {}
            for user_id, activities in self.eca.items():
                if self.users.get(user_id, {}).get("role") == "student":
                    eca_counts[user_id] = len(activities)

            grades_avg = {}
            for user_id, user_info in self.users.items():
                if user_info.get("role") != "student":
                    continue
                grades = self.grades.get(user_id)
                if grades is None:
                    continue
                avg = sum(grades) / len(grades)
                grades_avg[user_id] = avg

            data = {}
            for user_id in self.users:
                if self.users[user_id].get("role") != "student":
                    continue
                eca = eca_counts.get(user_id)
                mean = grades_avg.get(user_id)
                if eca is not None and mean is not None:
                    data[user_id] = [eca, mean]

            if not data:
                print("Insufficient data to display chart.")
                return

            df = pd.DataFrame.from_dict(data, orient="index", columns=["ECA Count", "Average Grade"])
            plt.figure(figsize=(7, 5))
            plt.plot(df["ECA Count"], df["Average Grade"], marker='o', linestyle='-', color='blue')
            plt.xlabel("ECA Participation Count")
            plt.ylabel("Average Grade")
            plt.title("ECA vs Academic Performance (Students Only)")
            plt.grid(True, linestyle='--', alpha=0.3)
            plt.tight_layout()
            plt.show()

        elif choice == "3":
            print("\nPerformance Summary: Passed vs Failed")
            threshold = 40
            passed = 0
            failed = 0

            for marks in self.grades.values():
                if all(mark >= threshold for mark in marks):
                    passed += 1
                else:
                    failed += 1

            labels = ['Passed', 'Failed']
            counts = [passed, failed]
            colors = ['green', 'red']

            plt.figure(figsize=(6, 4))
            plt.bar(labels, counts, color=colors)
            plt.title("Number of Passed vs Failed Students")
            plt.ylabel("Number of Students")
            plt.ylim(0, max(counts) + 1)
            plt.grid(axis='y', linestyle='--', alpha=0.3)
            plt.tight_layout()
            plt.show()
        else:
            print("Invalid option.")
# main function of the program
    def run(self):
        person = self.login()
        while True:
            person.menu()
            choice = input("Choose option: ").strip()
            if person.role == "admin":
                if choice == "1":
                    person.add_user(self)
                elif choice=="2":
                    person.update_user(self)
                elif choice == "3":
                    person.delete_user(self)
                elif choice == "4":
                    person.view_users(self)
                elif choice == "5":
                    person.data_insights(self)
                elif choice == "6":
                    print("Logging out...")
                    break
                else:
                    print("Invalid option. Try again.")
            else:
                if choice == "1":
                    person.view_profile(self)
                elif choice == "2":
                    person.view_grades(self)
                elif choice == "3":
                    person.view_eca(self)
                elif choice == "4":
                    print("Logging out...")
                    break
                else:
                    print("Invalid option. Try again.")



# Base Class named Person
class Person:
    def __init__(self, user_id, name, role, phone):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.contact = phone

    def menu(self):
        pass


#Class for Admin from the base class Person
class Admin(Person):
    def menu(self):
        print("\n1. Add user")
        print("2. Update user")
        print("3. Delete user")
        print("4. View Users")
        print("5. Data insights")
        print("6. Logout")
# adding user in the txt file.
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
                g = g.strip()
                if g.isdigit():
                    grades.append(int(g))
            eca_input = input("Enter ECA : ").strip()
            activities = []
            for e in eca_input.split(','):
                e=e.strip()
                if e:
                    activities.append(e)
            system.append_grades(user_id, grades)
            system.append_eca(user_id, activities)
# updating the user in the file.
    def update_user(self,system):
        print("----Update User----")
        user_id=input("Enter the user id to update:").strip()
        if user_id not in system.users or system.users[user_id]["role"]!='student':
            print("Invalid ID!")
        print("\nWhat do you like to update: ")
        print("1.Student info")
        print("2.Grades")
        print("3.ECA")
        choice=input("Enter your choice:")
        if choice=="1":
            name=input("Update the name or leave it empty").strip()
            contact=input("Update the contact or leave it empty").strip()
            password=input("Update the password or leave it empty").strip()
            if name:
                system.users[user_id]['name']=name
            if contact:
                system.users[user_id]['contact']=contact
            if password:
                system.users[user_id]['password']=password
            system.save_all()
        elif choice == "2":
            grades_input = input("Enter new grades: ").strip()
            try:
                grades = list(map(int, grades_input.split(",")))
                system.grades[user_id] = grades
                system.save_all()
            except Exception as e:
                print("Error updating grades:", e)
        elif choice == "3":
            eca_input = input("Enter new ECA activities: ").strip()
            try:
                activities = list(map(str.strip, eca_input.split(",")))
                system.eca[user_id] = activities
                system.save_all()
                print("ECA updated successfully.")
            except Exception as e:
                print("Error updating ECA:", e)

        else:
            print("Invalid option.")
#deleting the user from the file.
    def delete_user(self, system):
        user_id = input("Enter the user id:").strip()
        system.delete_user(user_id)
#viewing the user from the file.
    def view_users(self, system):
        system.view_users()
#providing the data insights.
    def data_insights(self, system):
        system.data_insights()


#Class for student from the base class Person
class Student(Person):
    def menu(self):
        print("\n1.View Profile")
        print("2.View Grades")
        print("3.View ECA")
        print("4.Sign out")
# viewing info of the students
    def view_profile(self, system):
        self_info = system.users[self.user_id]
        print("**** Your Details ****")
        print("\n--- MY PROFILE ---")
        print(f"ID      : {self.user_id}")
        print(f"Name    : {self_info['name']}")
        print(f"Role    : {self_info['role']}")
        print(f"Contact : {self_info['contact']}\n")

# viewing grades of the students
    def view_grades(self, system):
        print("\n--- MY GRADES ---")
        try:
            print("FOM,FODS,IT,English,ITF")
            g = system.grades[self.user_id]
            print(g)
        except KeyError:
            print("No grades on file.")
        print()
#viewing ECA of the students
    def view_eca(self, system):
        print("\n--- MY ECA ---")
        try:
            e = system.eca[self.user_id]
            print(e)
        except KeyError:
            print("No ECA activities on file.")
        print()


# Main program
if __name__ == "__main__":
    system = System_management()
    system.run()
