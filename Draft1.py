import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ----- File names -----
USER_FILE = "users.csv"
COURSE_FILE = "courses.csv"
STUDENT_FILE = "students.csv"


class GradeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("College Grade Tracking System")
        self.root.geometry("900x700")
        self.current_user = None

        self.ensure_files()
        self.create_login_page()

    # ----------------- File initialization -----------------
    def ensure_files(self):
        # users.csv header
        if not os.path.exists(USER_FILE):
            with open(USER_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Username", "Password", "Role"])
            # create a default admin for convenience
            with open(USER_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["admin", "admin", "admin"])

        # courses.csv header
        if not os.path.exists(COURSE_FILE):
            with open(COURSE_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["CourseCode", "CourseName"])

        # students.csv header (one row per student-course)
        if not os.path.exists(STUDENT_FILE):
            with open(STUDENT_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "CourseCode", "Marks", "Grade"])

    # ----------------- Login / Signup -----------------
    def create_login_page(self):
        for w in self.root.winfo_children():
            w.destroy()

        frame = tk.Frame(self.root, pady=20)
        frame.pack()

        tk.Label(frame, text="College Grade Tracking System", font=("Arial", 24, "bold")).pack(pady=10)
        tk.Label(frame, text="Login", font=("Arial", 18)).pack(pady=8)

        tk.Label(frame, text="Username").pack()
        self.login_username = tk.Entry(frame)
        self.login_username.pack(pady=4)

        tk.Label(frame, text="Password").pack()
        self.login_password = tk.Entry(frame, show="*")
        self.login_password.pack(pady=4)

        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Login", width=14, command=self.login_user).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Sign Up", width=14, command=self.create_signup_page).grid(row=0, column=1, padx=6)

    def create_signup_page(self):
        for w in self.root.winfo_children():
            w.destroy()

        frame = tk.Frame(self.root, pady=20)
        frame.pack()
        tk.Label(frame, text="Sign Up", font=("Arial", 20)).pack(pady=8)

        tk.Label(frame, text="Username").pack()
        self.signup_username = tk.Entry(frame)
        self.signup_username.pack(pady=4)

        tk.Label(frame, text="Password").pack()
        self.signup_password = tk.Entry(frame, show="*")
        self.signup_password.pack(pady=4)

        tk.Label(frame, text="Role (admin/student)").pack()
        self.signup_role = tk.Entry(frame)
        self.signup_role.pack(pady=4)

        tk.Button(frame, text="Register", width=16, command=self.register_user).pack(pady=8)
        tk.Button(frame, text="Back to Login", width=16, command=self.create_login_page).pack()

    def register_user(self):
        uname = self.signup_username.get().strip()
        pwd = self.signup_password.get().strip()
        role = self.signup_role.get().strip().lower()
        if not (uname and pwd and role in ("admin", "student")):
            messagebox.showerror("Error", "Enter username, password and role (admin or student).")
            return

        # check duplicate
        with open(USER_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            for r in reader:
                if r and r[0] == uname:
                    messagebox.showerror("Error", "Username already exists.")
                    return

        with open(USER_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([uname, pwd, role])

        messagebox.showinfo("Success", "Account created. You can log in.")
        self.create_login_page()

    def login_user(self):
        uname = self.login_username.get().strip()
        pwd = self.login_password.get().strip()
        found = False
        with open(USER_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            for r in reader:
                if r and r[0] == uname and r[1] == pwd:
                    self.current_user = {"username": uname, "role": r[2]}
                    found = True
                    break
        if not found:
            messagebox.showerror("Login failed", "Invalid username or password.")
            return

        if self.current_user["role"] == "admin":
            self.create_admin_home()
        else:
            self.create_student_home()

    # ----------------- Admin / Student Home -----------------
    def create_admin_home(self):
        for w in self.root.winfo_children():
            w.destroy()

        tk.Label(self.root, text=f"Admin Dashboard ( {self.current_user['username']} )", font=("Arial", 20, "bold")).pack(pady=12)
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=12)

        tk.Button(btn_frame, text="Manage Courses", width=20, command=self.manage_courses_page).grid(row=0, column=0, padx=6, pady=6)
        tk.Button(btn_frame, text="Add / Update Student Grade", width=20, command=self.add_student_grade_page).grid(row=0, column=1, padx=6, pady=6)
        tk.Button(btn_frame, text="Edit / Delete Student Records", width=22, command=self.edit_delete_page).grid(row=0, column=2, padx=6, pady=6)
        tk.Button(btn_frame, text="Generate Student Report (by ID)", width=22, command=self.generate_report_page).grid(row=1, column=0, padx=6, pady=6)
        tk.Button(btn_frame, text="All Students Report (table)", width=22, command=self.all_students_report).grid(row=1, column=1, padx=6, pady=6)
        tk.Button(btn_frame, text="Logout", width=20, command=self.logout).grid(row=1, column=2, padx=6, pady=6)

    def create_student_home(self):
        for w in self.root.winfo_children():
            w.destroy()

        tk.Label(self.root, text=f"Student Dashboard ( {self.current_user['username']} )", font=("Arial", 20, "bold")).pack(pady=12)
        tk.Button(self.root, text="View My Performance Report", width=30, command=self.student_view_own_report).pack(pady=8)
        tk.Button(self.root, text="Logout", width=30, command=self.logout).pack(pady=8)

    def logout(self):
        self.current_user = None
        self.create_login_page()

    # ----------------- Course Management (Admin) -----------------
    def manage_courses_page(self):
        for w in self.root.winfo_children():
            w.destroy()

        tk.Label(self.root, text="Manage Courses", font=("Arial", 18, "bold")).pack(pady=8)
        frame = tk.Frame(self.root)
        frame.pack(pady=8)

        tk.Label(frame, text="Course Code").grid(row=0, column=0, padx=6, pady=4)
        self.course_code_e = tk.Entry(frame)
        self.course_code_e.grid(row=0, column=1, padx=6, pady=4)

        tk.Label(frame, text="Course Name").grid(row=1, column=0, padx=6, pady=4)
        self.course_name_e = tk.Entry(frame, width=40)
        self.course_name_e.grid(row=1, column=1, padx=6, pady=4)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=6)
        tk.Button(btn_frame, text="Add Course", command=self.add_course).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Back", command=self.create_admin_home).grid(row=0, column=1, padx=6)

        # list existing courses
        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=10, fill="both", expand=False)
        tk.Label(list_frame, text="Existing courses:", font=("Arial", 12, "bold")).pack(anchor="w")
        courses_box = tk.Text(list_frame, height=8, width=80)
        courses_box.pack(pady=6)
        courses_box.config(state="normal")
        courses_box.delete("1.0", tk.END)
        with open(COURSE_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            for r in reader:
                if r:
                    courses_box.insert(tk.END, f"{r[0]}  -  {r[1]}\n")
        courses_box.config(state="disabled")

    def add_course(self):
        code = (self.course_code_e.get() or "").strip().upper()
        name = (self.course_name_e.get() or "").strip()
        if not (code and name):
            messagebox.showerror("Input error", "Enter both course code and name.")
            return

        # check duplicates
        with open(COURSE_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            for r in reader:
                if r and r[0] == code:
                    messagebox.showerror("Duplicate", "Course code already exists.")
                    return

        with open(COURSE_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([code, name])

        messagebox.showinfo("Success", f"Course {code} added.")
        self.manage_courses_page()

    # ----------------- Add / Update Student Grade -----------------
    def add_student_grade_page(self):
        for w in self.root.winfo_children():
            w.destroy()

        tk.Label(self.root, text="Add / Update Student Grade", font=("Arial", 18, "bold")).pack(pady=8)
        frame = tk.Frame(self.root)
        frame.pack(pady=8)

        tk.Label(frame, text="Student ID").grid(row=0, column=0, padx=6, pady=4)
        self.as_sid = tk.Entry(frame)
        self.as_sid.grid(row=0, column=1, padx=6, pady=4)

        tk.Label(frame, text="Student Name").grid(row=1, column=0, padx=6, pady=4)
        self.as_name = tk.Entry(frame)
        self.as_name.grid(row=1, column=1, padx=6, pady=4)

        tk.Label(frame, text="Course Code").grid(row=2, column=0, padx=6, pady=4)
        self.as_course = tk.Entry(frame)
        self.as_course.grid(row=2, column=1, padx=6, pady=4)

        tk.Label(frame, text="Marks").grid(row=3, column=0, padx=6, pady=4)
        self.as_marks = tk.Entry(frame)
        self.as_marks.grid(row=3, column=1, padx=6, pady=4)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Save / Update", command=self.save_student_grade).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Back", command=self.create_admin_home).grid(row=0, column=1, padx=6)

    def save_student_grade(self):
        sid = (self.as_sid.get() or "").strip()
        name = (self.as_name.get() or "").strip()
        course = (self.as_course.get() or "").strip().upper()
        marks_raw = (self.as_marks.get() or "").strip()
        if not (sid and name and course and marks_raw):
            messagebox.showerror("Input error", "All fields required.")
            return

        # validate course exists
        course_exists = False
        with open(COURSE_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            for r in reader:
                if r and r[0] == course:
                    course_exists = True
                    break
        if not course_exists:
            messagebox.showerror("Course missing", "Course code not found. Add it first.")
            return

        try:
            marks = float(marks_raw)
        except ValueError:
            messagebox.showerror("Marks error", "Enter numeric marks.")
            return

        grade = self.marks_to_grade(marks)

        # Read all records and update if student+course exists, else append
        rows = []
        updated = False
        with open(STUDENT_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)

        # ensure header exists (safe rewrite)
        if not rows:
            rows = [["ID", "Name", "CourseCode", "Marks", "Grade"]]

        # search (skip header)
        for i, row in enumerate(rows):
            if i == 0:
                continue
            if row and row[0] == sid and row[2] == course:
                rows[i] = [sid, name, course, f"{marks:.2f}", grade]
                updated = True

        if updated:
            # write back
            with open(STUDENT_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            messagebox.showinfo("Updated", f"Updated marks for {sid} - {course}.")
        else:
            # append
            with open(STUDENT_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([sid, name, course, f"{marks:.2f}", grade])
            messagebox.showinfo("Saved", f"Saved record for {sid} - {course}.")

        # clear inputs
        self.as_sid.delete(0, tk.END)
        self.as_name.delete(0, tk.END)
        self.as_course.delete(0, tk.END)
        self.as_marks.delete(0, tk.END)

    # ----------------- Edit / Delete Student Records -----------------
    def edit_delete_page(self):
        for w in self.root.winfo_children():
            w.destroy()

        tk.Label(self.root, text="Edit / Delete Student Records", font=("Arial", 18, "bold")).pack(pady=8)
        frame = tk.Frame(self.root)
        frame.pack(pady=8)
        tk.Label(frame, text="Enter Student ID").grid(row=0, column=0, padx=6, pady=4)
        self.ed_search_id = tk.Entry(frame)
        self.ed_search_id.grid(row=0, column=1, padx=6, pady=4)
        tk.Button(frame, text="Search", command=self.search_student_records).grid(row=0, column=2, padx=6)
        tk.Button(frame, text="Back", command=self.create_admin_home).grid(row=1, column=1, pady=8)

    def search_student_records(self):
        sid = (self.ed_search_id.get() or "").strip()
        if not sid:
            messagebox.showerror("Input error", "Enter student ID.")
            return

        with open(STUDENT_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            records = [r for r in reader if r and r[0] == sid]

        if not records:
            messagebox.showerror("Not found", "No records for this student ID.")
            return

        # open a new window listing course rows with Edit/Delete buttons
        win = tk.Toplevel(self.root)
        win.title(f"Records for {sid}")
        tk.Label(win, text=f"Student ID: {sid}  |  Name: {records[0][1]}", font=("Arial", 14, "bold")).pack(pady=8)

        for rec in records:
            frame = tk.Frame(win, pady=4)
            frame.pack(fill="x", padx=8)
            lbl = tk.Label(frame, text=f"{rec[2]}  -  Marks: {rec[3]}  |  Grade: {rec[4]}", anchor="w")
            lbl.pack(side="left", padx=6)
            tk.Button(frame, text="Edit", command=lambda r=rec, w=win: self.open_edit_marks_window(r, w)).pack(side="right", padx=6)
            tk.Button(frame, text="Delete", command=lambda r=rec, w=win: self.delete_course_record(r, w)).pack(side="right", padx=6)

    def open_edit_marks_window(self, record, parent_win):
        # record: [ID, Name, CourseCode, Marks, Grade]
        ew = tk.Toplevel(parent_win)
        ew.title(f"Edit {record[2]} for {record[0]}")
        tk.Label(ew, text=f"Editing {record[2]} for {record[1]}", font=("Arial", 12, "bold")).pack(pady=6)
        tk.Label(ew, text="New Marks").pack()
        new_marks_e = tk.Entry(ew)
        new_marks_e.pack(pady=6)
        new_marks_e.insert(0, record[3])

        def save_edit():
            val = new_marks_e.get().strip()
            try:
                nm = float(val)
            except ValueError:
                messagebox.showerror("Input error", "Enter numeric marks.")
                return
            new_grade = self.marks_to_grade(nm)
            # read all and update
            with open(STUDENT_FILE, "r", newline="") as f:
                rows = list(csv.reader(f))
            for i, r in enumerate(rows):
                if i == 0:  # header
                    continue
                if r and r[0] == record[0] and r[2] == record[2]:
                    rows[i][3] = f"{nm:.2f}"
                    rows[i][4] = new_grade
            with open(STUDENT_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            messagebox.showinfo("Saved", "Marks updated.")
            ew.destroy()
            parent_win.destroy()

        tk.Button(ew, text="Save", command=save_edit).pack(pady=6)

    def delete_course_record(self, record, parent_win):
        # remove that row and rewrite csv
        with open(STUDENT_FILE, "r", newline="") as f:
            rows = list(csv.reader(f))
        new_rows = [r for r in rows if not (r and r[0] == record[0] and r[2] == record[2])]
        with open(STUDENT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(new_rows)
        messagebox.showinfo("Deleted", f"Deleted {record[2]} for {record[0]}.")
        parent_win.destroy()

    # ----------------- Reports -----------------
    def generate_report_page(self):
        for w in self.root.winfo_children():
            w.destroy()

        tk.Label(self.root, text="Generate Student Report (by ID)", font=("Arial", 18, "bold")).pack(pady=8)
        frame = tk.Frame(self.root)
        frame.pack(pady=6)
        tk.Label(frame, text="Student ID").grid(row=0, column=0, padx=6)
        self.rp_student_id = tk.Entry(frame)
        self.rp_student_id.grid(row=0, column=1, padx=6)
        tk.Button(frame, text="Generate", command=self.generate_student_report_by_id).grid(row=0, column=2, padx=6)
        tk.Button(self.root, text="Back", command=self.create_admin_home).pack(pady=8)

    def generate_student_report_by_id(self):
        sid = (self.rp_student_id.get() or "").strip()
        if not sid:
            messagebox.showerror("Input", "Enter student ID.")
            return
        with open(STUDENT_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            recs = [r for r in reader if r and r[0] == sid]
        if not recs:
            messagebox.showerror("Not found", "No records for this ID.")
            return
        self.show_student_report(recs)

    def student_view_own_report(self):
        # student username is expected to be their ID in this design (common pattern)
        sid = self.current_user["username"]
        with open(STUDENT_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            recs = [r for r in reader if r and r[0] == sid]
        if not recs:
            messagebox.showerror("No records", "No records found for your ID.")
            return
        self.show_student_report(recs)

    def show_student_report(self, recs):
        # recs: list of [ID, Name, CourseCode, Marks, Grade]
        win = tk.Toplevel(self.root)
        win.title(f"Performance Report - {recs[0][1]} ({recs[0][0]})")
        win.geometry("850x700")

        tk.Label(win, text=f"{recs[0][1]}  —  {recs[0][0]}", font=("Arial", 16, "bold")).pack(pady=8)

        # course listing
        list_frame = tk.Frame(win)
        list_frame.pack(pady=6)
        tk.Label(list_frame, text="Course - Marks - Grade", font=("Arial", 12, "bold")).pack(anchor="w")
        for r in recs:
            tk.Label(list_frame, text=f"{r[2]}  |  Marks: {r[3]}  |  Grade: {r[4]}", anchor="w").pack(anchor="w")

        # marks and grades arrays
        marks = [float(r[3]) for r in recs]
        grades = [r[4] for r in recs]

        avg_marks = sum(marks) / len(marks)
        highest = max(marks)
        lowest = min(marks)
        # compute GPA (average of grade points)
        gpa = self.compute_gpa_for_records(recs)

        stats_frame = tk.Frame(win)
        stats_frame.pack(pady=8)
        tk.Label(stats_frame, text=f"Average Marks: {avg_marks:.2f}", font=("Arial", 12)).grid(row=0, column=0, padx=8, pady=4)
        tk.Label(stats_frame, text=f"Highest: {highest:.2f}", font=("Arial", 12)).grid(row=0, column=1, padx=8, pady=4)
        tk.Label(stats_frame, text=f"Lowest: {lowest:.2f}", font=("Arial", 12)).grid(row=0, column=2, padx=8, pady=4)
        tk.Label(stats_frame, text=f"GPA: {gpa:.2f}", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=8, pady=4)

        # Pie chart for subject-wise marks distribution
        subjects = [r[2] for r in recs]
        fig, ax = plt.subplots(figsize=(5, 4))
        # if all marks zero or identical matplotlib handles; show percentages
        ax.pie(marks, labels=subjects, autopct="%1.1f%%", startangle=90)
        ax.set_title("Subject-wise Marks Distribution")
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        tk.Button(win, text="Close", command=win.destroy).pack(pady=6)

    # ----------------- All Students Report Table (Admin) -----------------
    def all_students_report(self):
        # aggregate per student: collect records, compute GPA, avg marks, count
        students = {}  # sid -> {"name": name, "marks": [...], "grades":[...]}
        with open(STUDENT_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            for r in reader:
                if not r:
                    continue
                sid, name, course, marks_s, grade = r[0], r[1], r[2], r[3], r[4]
                try:
                    marks = float(marks_s)
                except:
                    continue
                if sid not in students:
                    students[sid] = {"name": name, "marks": [], "grades": []}
                students[sid]["marks"].append(marks)
                students[sid]["grades"].append(grade)

        # open new window with treeview
        win = tk.Toplevel(self.root)
        win.title("All Students Report")
        win.geometry("900x600")
        tk.Label(win, text="All Students Report", font=("Arial", 16, "bold")).pack(pady=8)

        cols = ("Student ID", "Name", "Courses Count", "Avg Marks", "GPA")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=18)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=160, anchor="center")
        tree.pack(pady=8, fill="both", expand=True)

        # populate rows
        for sid, info in students.items():
            avg_marks = sum(info["marks"]) / len(info["marks"])
            # compute gpa
            # map grades to points and average
            gpa = self.compute_gpa_for_grade_list(info["grades"])
            tree.insert("", tk.END, values=(sid, info["name"], len(info["marks"]), f"{avg_marks:.2f}", f"{gpa:.2f}"))

        # button frame for export/close if desired
        btnf = tk.Frame(win)
        btnf.pack(pady=8)
        tk.Button(btnf, text="Close", command=win.destroy).pack()

    # ----------------- Grade mappings -----------------
    def marks_to_grade(self, marks: float) -> str:
        # Grading system requested:
        # S: >=90
        # A: 80-89
        # B: 70-79
        # C: 60-69
        # D: 50-59
        # F: <50
        if marks >= 90:
            return "S"
        elif marks >= 80:
            return "A"
        elif marks >= 70:
            return "B"
        elif marks >= 60:
            return "C"
        elif marks >= 50:
            return "D"
        else:
            return "F"

    def grade_to_gpa_point(self, grade: str) -> float:
        # S=5, A=4, B=3, C=2, D=1, F=0
        mapping = {"S": 5.0, "A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}
        return mapping.get(grade.upper(), 0.0)

    def compute_gpa_for_records(self, recs) -> float:
        # recs: list of rows [ID, Name, CourseCode, Marks, Grade]
        points = [self.grade_to_gpa_point(r[4]) for r in recs]
        if not points:
            return 0.0
        return sum(points) / len(points)

    def compute_gpa_for_grade_list(self, grade_list) -> float:
        points = [self.grade_to_gpa_point(g) for g in grade_list]
        if not points:
            return 0.0
        return sum(points) / len(points)

    # ----------------- Utility / Main loop -----------------
def main():
    root = tk.Tk()
    app = GradeTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
