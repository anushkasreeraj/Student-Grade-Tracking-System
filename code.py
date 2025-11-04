import tkinter as tk
from tkinter import messagebox
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ===== FILE NAMES =====
STUDENT_FILE = 'students.csv'
USER_FILE = 'users.csv'


class GradeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Tracker")
        self.root.geometry("600x500")

        self.current_user = None
        self.create_login_page()
        self.initialize_files()

    def initialize_files(self):
        if not os.path.exists(STUDENT_FILE):
            with open(STUDENT_FILE, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Subject 1", "Subject 2", "Subject 3", "Subject 4", "Grade"])

        if not os.path.exists(USER_FILE):
            with open(USER_FILE, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Username", "Password", "Role"])

    # ================= LOGIN / SIGNUP =================
    def create_login_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Login", font=("Arial", 24, "bold")).pack(pady=20)

        tk.Label(self.root, text="Username:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", width=15, command=self.login).pack(pady=10)
        tk.Button(self.root, text="Sign Up", width=15, command=self.create_signup_page).pack(pady=5)

    def create_signup_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Sign Up", font=("Arial", 24, "bold")).pack(pady=20)

        tk.Label(self.root, text="Username:").pack()
        self.new_username_entry = tk.Entry(self.root)
        self.new_username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack()
        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_password_entry.pack(pady=5)

        tk.Label(self.root, text="Role (admin/student):").pack()
        self.role_entry = tk.Entry(self.root)
        self.role_entry.pack(pady=5)

        tk.Button(self.root, text="Sign Up", width=15, command=self.signup).pack(pady=10)
        tk.Button(self.root, text="Back to Login", width=15, command=self.create_login_page).pack(pady=5)

    def signup(self):
        username = self.new_username_entry.get().strip()
        password = self.new_password_entry.get().strip()
        role = self.role_entry.get().strip().lower()

        if not username or not password or role not in ["admin", "student"]:
            messagebox.showerror("Error", "Invalid input! Role must be 'admin' or 'student'.")
            return

        with open(USER_FILE, mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == username:
                    messagebox.showerror("Error", "Username already exists!")
                    return

        with open(USER_FILE, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, password, role])

        messagebox.showinfo("Success", "Sign up successful! You can now log in.")
        self.create_login_page()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        with open(USER_FILE, mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == username and row[1] == password:
                    self.current_user = {"username": username, "role": row[2]}
                    messagebox.showinfo("Login Successful", f"Welcome, {username} ({row[2]})")
                    self.create_home_page()
                    return

        messagebox.showerror("Error", "Invalid username or password!")

    # ================= MAIN HOME PAGE =================
    def create_home_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Welcome {self.current_user['username']}!", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.root, text="Student Grade Tracker", font=("Arial", 20, "bold")).pack(pady=10)

        if self.current_user['role'] == "admin":
            tk.Button(self.root, text="Add Student Record", width=25, command=self.add_student_page).pack(pady=10)
            tk.Button(self.root, text="Edit/Delete Student Record", width=25, command=self.edit_delete_page).pack(pady=10)
            tk.Button(self.root, text="View All Records", width=25, command=self.view_all_records).pack(pady=10)
            tk.Button(self.root, text="Generate Performance Report", width=25, command=self.report_input_page).pack(pady=10)
        else:
            tk.Button(self.root, text="View All Records", width=25, command=self.view_all_records).pack(pady=10)
            tk.Button(self.root, text="View My Performance Report", width=25, command=self.report_input_page).pack(pady=10)

        tk.Button(self.root, text="Logout", width=15, command=self.create_login_page).pack(pady=10)

    # ================= ADD STUDENT =================
    def add_student_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Add Student Record", font=("Arial", 20, "bold")).pack(pady=20)

        labels = ["Student ID", "Student Name", "Subject 1", "Subject 2", "Subject 3", "Subject 4"]
        self.entries = {}
        for label in labels:
            tk.Label(self.root, text=label).pack()
            self.entries[label] = tk.Entry(self.root)
            self.entries[label].pack(pady=3)

        tk.Button(self.root, text="Save", command=self.save_student).pack(pady=15)
        tk.Button(self.root, text="Back to Home", command=self.create_home_page).pack(pady=5)

    def save_student(self):
        try:
            student_id = self.entries["Student ID"].get()
            name = self.entries["Student Name"].get()
            marks = [float(self.entries[f"Subject {i}"].get()) for i in range(1, 5)]
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric grades.")
            return

        avg = sum(marks) / 4
        grade = self.calculate_grade(avg)

        with open(STUDENT_FILE, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([student_id, name, *marks, grade])

        messagebox.showinfo("Success", "Student record added!")
        self.create_home_page()

    # ================= EDIT / DELETE =================
    def edit_delete_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Edit/Delete Student Record", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(self.root, text="Enter Student ID:").pack()
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack(pady=5)

        tk.Button(self.root, text="Search", command=self.search_student).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_home_page).pack(pady=10)

    def search_student(self):
        sid = self.search_entry.get().strip()
        with open(STUDENT_FILE, mode='r') as f:
            reader = csv.reader(f)
            data = list(reader)

        for row in data:
            if row and row[0] == sid:
                self.show_edit_page(row)
                return
        messagebox.showerror("Error", "Student not found!")

    def show_edit_page(self, student_data):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Edit Student Record", font=("Arial", 20, "bold")).pack(pady=20)

        fields = ["ID", "Name", "Subject 1", "Subject 2", "Subject 3", "Subject 4"]
        self.edit_entries = {}
        for i, field in enumerate(fields):
            tk.Label(self.root, text=field).pack()
            e = tk.Entry(self.root)
            e.insert(0, student_data[i])
            e.pack(pady=3)
            self.edit_entries[field] = e

        tk.Button(self.root, text="Save Changes", command=lambda: self.save_edited_student(student_data[0])).pack(pady=10)
        tk.Button(self.root, text="Delete Record", command=lambda: self.delete_student(student_data[0])).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_home_page).pack(pady=10)

    def save_edited_student(self, old_id):
        updated_data = [self.edit_entries["ID"].get(), self.edit_entries["Name"].get()]
        try:
            marks = [float(self.edit_entries[f"Subject {i}"].get()) for i in range(1, 5)]
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric grades.")
            return

        avg = sum(marks) / 4
        grade = self.calculate_grade(avg)
        updated_data.extend(marks)
        updated_data.append(grade)

        with open(STUDENT_FILE, mode='r') as f:
            data = list(csv.reader(f))

        with open(STUDENT_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            for row in data:
                if row and row[0] == old_id:
                    writer.writerow(updated_data)
                else:
                    writer.writerow(row)

        messagebox.showinfo("Success", "Record updated successfully!")
        self.create_home_page()

    def delete_student(self, sid):
        with open(STUDENT_FILE, mode='r') as f:
            data = list(csv.reader(f))

        with open(STUDENT_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            for row in data:
                if row and row[0] != sid:
                    writer.writerow(row)

        messagebox.showinfo("Deleted", "Record deleted successfully!")
        self.create_home_page()

    # ================= VIEW & REPORT =================
    def view_all_records(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="All Student Records", font=("Arial", 20, "bold")).pack(pady=20)

        with open(STUDENT_FILE, mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] != "ID":
                    tk.Label(self.root, text=f"ID: {row[0]}, Name: {row[1]}, Grade: {row[6]}").pack()

        tk.Button(self.root, text="Back", command=self.create_home_page).pack(pady=10)

    def report_input_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Performance Report", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(self.root, text="Enter Student ID:").pack(pady=5)

        self.report_id_entry = tk.Entry(self.root)
        self.report_id_entry.pack(pady=5)

        tk.Button(self.root, text="Generate Report", command=self.generate_student_report).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_home_page).pack(pady=10)

    def generate_student_report(self):
        sid = self.report_id_entry.get().strip()
        with open(STUDENT_FILE, mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == sid:
                    self.show_student_report(row)
                    return
        messagebox.showerror("Error", "Student not found!")

    def show_student_report(self, student_data):
        report_win = tk.Toplevel(self.root)
        report_win.title(f"Performance Report - {student_data[1]}")
        report_win.geometry("600x600")

        try:
            marks = [float(student_data[i]) for i in range(2, 6)]
        except:
            messagebox.showerror("Error", "Invalid marks in record!")
            return

        avg = sum(marks) / 4
        gpa = (avg / 20)  # Assuming 100 marks → 5 GPA scale
        highest = max(marks)
        lowest = min(marks)

        tk.Label(report_win, text=f"Name: {student_data[1]}", font=("Arial", 16)).pack(pady=5)
        tk.Label(report_win, text=f"Average Marks: {avg:.2f}", font=("Arial", 14)).pack(pady=5)
        tk.Label(report_win, text=f"Grade: {student_data[6]}", font=("Arial", 14)).pack(pady=5)
        tk.Label(report_win, text=f"GPA: {gpa:.2f}", font=("Arial", 14)).pack(pady=5)
        tk.Label(report_win, text=f"Highest Marks: {highest}", font=("Arial", 14)).pack(pady=5)
        tk.Label(report_win, text=f"Lowest Marks: {lowest}", font=("Arial", 14)).pack(pady=5)

        # Create pie chart for marks distribution
        fig, ax = plt.subplots(figsize=(4, 4))
        subjects = ["Subject 1", "Subject 2", "Subject 3", "Subject 4"]
        ax.pie(marks, labels=subjects, autopct="%1.1f%%", startangle=90)
        ax.set_title("Subject-wise Marks Distribution")

        chart = FigureCanvasTkAgg(fig, master=report_win)
        chart.draw()
        chart.get_tk_widget().pack(pady=10)

        tk.Button(report_win, text="Close", command=report_win.destroy).pack(pady=10)

    # ================= HELPER =================
    def calculate_grade(self, avg):
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        else:
            return "F"


if __name__ == "__main__":
    root = tk.Tk()
    app = GradeTrackerApp(root)
    root.mainloop()
