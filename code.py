import tkinter as tk
from tkinter import messagebox
import csv
import os


# Define the file name for storing student data
STUDENT_FILE = 'students.csv'


# Create the main class for the system
class GradeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Tracker")
        self.root.geometry("600x400")

        # Initialize the main window
        self.create_home_page()

    def create_home_page(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Home page layout
        title_label = tk.Label(self.root, text="Student Grade Tracker", font=("Arial", 20))
        title_label.pack(pady=20)

        # Buttons for navigation
        add_btn = tk.Button(self.root, text="Add Student Record", width=20, command=self.add_student_page)
        add_btn.pack(pady=10)

        edit_btn = tk.Button(self.root, text="Edit/Delete Student Record", width=20, command=self.edit_delete_page)
        edit_btn.pack(pady=10)

        view_btn = tk.Button(self.root, text="View All Records", width=20, command=self.view_all_records)
        view_btn.pack(pady=10)

        report_btn = tk.Button(self.root, text="Generate Performance Report", width=20, command=self.generate_report)
        report_btn.pack(pady=10)

        self.load_student_data()

    def load_student_data(self):
        """ Load student data from CSV file """
        if not os.path.exists(STUDENT_FILE):
            with open(STUDENT_FILE, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Subject 1", "Subject 2", "Subject 3", "Subject 4", "Grade"])

    def add_student_page(self):
        # Clear the window and create the Add Student page
        for widget in self.root.winfo_children():
            widget.destroy()

        # Form elements to add a new student
        title_label = tk.Label(self.root, text="Add Student Record", font=("Arial", 20))
        title_label.pack(pady=20)

        # Student Name and ID fields
        tk.Label(self.root, text="Student ID").pack(pady=5)
        self.student_id_entry = tk.Entry(self.root)
        self.student_id_entry.pack(pady=5)

        tk.Label(self.root, text="Student Name").pack(pady=5)
        self.student_name_entry = tk.Entry(self.root)
        self.student_name_entry.pack(pady=5)

        # Subject grades fields
        tk.Label(self.root, text="Grade for Subject 1").pack(pady=5)
        self.subject1_entry = tk.Entry(self.root)
        self.subject1_entry.pack(pady=5)

        tk.Label(self.root, text="Grade for Subject 2").pack(pady=5)
        self.subject2_entry = tk.Entry(self.root)
        self.subject2_entry.pack(pady=5)

        tk.Label(self.root, text="Grade for Subject 3").pack(pady=5)
        self.subject3_entry = tk.Entry(self.root)
        self.subject3_entry.pack(pady=5)

        tk.Label(self.root, text="Grade for Subject 4").pack(pady=5)
        self.subject4_entry = tk.Entry(self.root)
        self.subject4_entry.pack(pady=5)

        # Save button
        save_btn = tk.Button(self.root, text="Save", command=self.save_student)
        save_btn.pack(pady=20)

        # Back to Home button
        back_btn = tk.Button(self.root, text="Back to Home", command=self.create_home_page)
        back_btn.pack(pady=10)

    def save_student(self):
        # Get the input values
        student_id = self.student_id_entry.get()
        student_name = self.student_name_entry.get()
        subject1 = self.subject1_entry.get()
        subject2 = self.subject2_entry.get()
        subject3 = self.subject3_entry.get()
        subject4 = self.subject4_entry.get()

        # Grade Calculation: Average of the 4 subjects
        try:
            grades = [float(subject1), float(subject2), float(subject3), float(subject4)]
            avg_grade = sum(grades) / len(grades)

            if avg_grade >= 90:
                grade = "A"
            elif avg_grade >= 80:
                grade = "B"
            elif avg_grade >= 70:
                grade = "C"
            elif avg_grade >= 60:
                grade = "D"
            else:
                grade = "F"
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for grades.")
            return

        # Save the student data in the CSV file
        with open(STUDENT_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([student_id, student_name, subject1, subject2, subject3, subject4, grade])

        messagebox.showinfo("Success", f"Student {student_name} has been added successfully!")
        self.create_home_page()

    def edit_delete_page(self):
        # Clear the window and create the Edit/Delete page
        for widget in self.root.winfo_children():
            widget.destroy()

        # Form to search for a student by ID
        title_label = tk.Label(self.root, text="Edit/Delete Student Record", font=("Arial", 20))
        title_label.pack(pady=20)

        tk.Label(self.root, text="Enter Student ID to search").pack(pady=5)
        self.search_id_entry = tk.Entry(self.root)
        self.search_id_entry.pack(pady=5)

        search_btn = tk.Button(self.root, text="Search", command=self.search_student)
        search_btn.pack(pady=10)

        # Back to Home button
        back_btn = tk.Button(self.root, text="Back to Home", command=self.create_home_page)
        back_btn.pack(pady=10)

    def search_student(self):
        student_id = self.search_id_entry.get()

        # Search for the student in the file
        with open(STUDENT_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == student_id:
                    self.show_student_details(row)
                    return
            messagebox.showerror("Not Found", "Student ID not found!")

    def show_student_details(self, student_data):
        # Clear the window and show student details with options to edit or delete
        for widget in self.root.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.root, text="Student Record", font=("Arial", 20))
        title_label.pack(pady=20)

        tk.Label(self.root, text=f"ID: {student_data[0]}").pack(pady=5)
        tk.Label(self.root, text=f"Name: {student_data[1]}").pack(pady=5)
        tk.Label(self.root, text=f"Subject 1: {student_data[2]}").pack(pady=5)
        tk.Label(self.root, text=f"Subject 2: {student_data[3]}").pack(pady=5)
        tk.Label(self.root, text=f"Subject 3: {student_data[4]}").pack(pady=5)
        tk.Label(self.root, text=f"Subject 4: {student_data[5]}").pack(pady=5)
        tk.Label(self.root, text=f"Grade: {student_data[6]}").pack(pady=5)

        # Buttons to edit or delete
        edit_btn = tk.Button(self.root, text="Edit", command=lambda: self.edit_student(student_data))
        edit_btn.pack(pady=10)

        delete_btn = tk.Button(self.root, text="Delete", command=lambda: self.delete_student(student_data[0]))
        delete_btn.pack(pady=10)

        # Back to Home button
        back_btn = tk.Button(self.root, text="Back to Home", command=self.create_home_page)
        back_btn.pack(pady=10)

    def edit_student(self, student_data):
        # Edit functionality (this part needs to be implemented)
        pass  # You can implement the edit functionality here

    def delete_student(self, student_id):
        # Remove the student from the CSV file
        rows = []
        with open(STUDENT_FILE, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)

        rows = [row for row in rows if row[0] != student_id]

        with open(STUDENT_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        messagebox.showinfo("Success", "Student record has been deleted!")
        self.create_home_page()

    def view_all_records(self):
        # Clear the window and show all student records
        for widget in self.root.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.root, text="All Student Records", font=("Arial", 20))
        title_label.pack(pady=20)

        with open(STUDENT_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                record_label = tk.Label(self.root, text=f"ID: {row[0]}, Name: {row[1]}, Grade: {row[6]}")
                record_label.pack(pady=5)

        # Back to Home button
        back_btn = tk.Button(self.root, text="Back to Home", command=self.create_home_page)
        back_btn.pack(pady=10)

    def generate_report(self):
        # Generate performance report (average grade for each student)
        with open(STUDENT_FILE, mode='r') as file:
            reader = csv.reader(file)
            report_data = []
            for row in reader:
                try:
                    grades = [float(row[2]), float(row[3]), float(row[4]), float(row[5])]
                    avg_grade = sum(grades) / len(grades)
                    report_data.append(f"ID: {row[0]}, Name: {row[1]}, Avg Grade: {avg_grade:.2f}, Grade: {row[6]}")
                except ValueError:
                    continue

        report_window = tk.Toplevel(self.root)
        report_window.title("Performance Report")

        for line in report_data:
            tk.Label(report_window, text=line).pack()

        back_btn = tk.Button(report_window, text="Close", command=report_window.destroy)
        back_btn.pack(pady=10)


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = GradeTrackerApp(root)
    root.mainloop()
