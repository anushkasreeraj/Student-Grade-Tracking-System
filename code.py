import tkinter as tk
from tkinter import messagebox, ttk
import csv, os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

# ----- File names -----
USER_FILE = "users.csv"
COURSE_FILE = "courses.csv"
STUDENT_FILE = "students.csv"

class GradeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grade Tracking System")
        self.root.geometry("1000x750")
        self.bg_cache = {}
        self.current_user = None

        self.ensure_files()
        self.create_login_page()

    # ---------- background helper ----------
    def set_background(self, window, image_file):
        if not os.path.exists(image_file):
            return
        img = Image.open(image_file)
        img = img.resize((1000, 750))
        bg = ImageTk.PhotoImage(img)
        self.bg_cache[image_file] = bg
        label = tk.Label(window, image=bg)
        label.place(x=0, y=0, relwidth=1, relheight=1)
        label.lower()

    # ---------- file initialization ----------
    def ensure_files(self):
        # ensure users file with header exists
        if not os.path.exists(USER_FILE):
            with open(USER_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Username", "Password", "Role"])
                writer.writerow(["admin", "admin", "admin"])
        else:
            # if exists but empty, write header
            if os.path.getsize(USER_FILE) == 0:
                with open(USER_FILE, "w", newline="") as f:
                    csv.writer(f).writerow(["Username", "Password", "Role"])
                    csv.writer(f).writerow(["admin", "admin", "admin"])

        if not os.path.exists(COURSE_FILE):
            with open(COURSE_FILE, "w", newline="") as f:
                csv.writer(f).writerow(["CourseCode", "CourseName"])

        if not os.path.exists(STUDENT_FILE):
            with open(STUDENT_FILE, "w", newline="") as f:
                csv.writer(f).writerow(["ID", "Name", "CourseCode", "Marks", "Grade"])

    # ---------- login/signup pages ----------
    def create_login_page(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.set_background(self.root, "login_bg.png")

        frame = tk.Frame(self.root, bg="white", padx=30, pady=30)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="College Grade Tracking System", font=("Arial", 24, "bold"), bg="white").pack(pady=10)
        tk.Label(frame, text="Login", font=("Arial", 18, "bold"), bg="white").pack(pady=8)

        tk.Label(frame, text="Username", font=("Arial", 12), bg="white").pack()
        self.login_username = tk.Entry(frame, font=("Arial", 12))
        self.login_username.pack(pady=5)

        tk.Label(frame, text="Password", font=("Arial", 12), bg="white").pack()
        self.login_password = tk.Entry(frame, show="*", font=("Arial", 12))
        self.login_password.pack(pady=5)

        tk.Button(frame, text="Login", bg="#053052", fg="white", font=("Arial", 12, "bold"), width=14,
                  command=self.login_user).pack(pady=10)
        tk.Button(frame, text="Sign Up", font=("Arial", 12), width=14,
                  command=self.create_signup_page).pack()

    def create_signup_page(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.set_background(self.root, "signup_bg.png")

        frame = tk.Frame(self.root, bg="white", padx=30, pady=30)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Create New Account", font=("Arial", 22, "bold"), bg="white").pack(pady=10)
        tk.Label(frame, text="Username", bg="white", font=("Arial", 12)).pack()
        self.signup_username = tk.Entry(frame, font=("Arial", 12))
        self.signup_username.pack(pady=5)
        tk.Label(frame, text="Password", bg="white", font=("Arial", 12)).pack()
        self.signup_password = tk.Entry(frame, show="*", font=("Arial", 12))
        self.signup_password.pack(pady=5)
        tk.Label(frame, text="Role (admin/student)", bg="white", font=("Arial", 12)).pack()
        self.signup_role = tk.Entry(frame, font=("Arial", 12))
        self.signup_role.pack(pady=5)
        tk.Button(frame, text="Register", font=("Arial", 12, "bold"), width=14, command=self.register_user).pack(pady=10)
        tk.Button(frame, text="Back to Login", font=("Arial", 12), width=14, command=self.create_login_page).pack()

    # ---------- safely read users.csv (handles header/no-header) ----------
    def _read_users(self):
        users = []
        # prefer DictReader but fallback to reader
        try:
            with open(USER_FILE, "r", newline="") as f:
                f.seek(0)
                rdr = csv.DictReader(f)
                # if DictReader has fieldnames and includes Username/Password
                if rdr.fieldnames and "Username" in rdr.fieldnames and "Password" in rdr.fieldnames:
                    for r in rdr:
                        if r and r.get("Username"):
                            users.append({"username": r.get("Username"), "password": r.get("Password"), "role": r.get("Role")})
                    return users
        except Exception:
            pass

        # fallback: plain reader, assume columns in order Username,Password,Role
        try:
            with open(USER_FILE, "r", newline="") as f:
                rdr = csv.reader(f)
                for r in rdr:
                    if not r:
                        continue
                    # ignore header row if it looks like header
                    if r[0].strip().lower() in ("username", "user", "uname"):
                        continue
                    if len(r) >= 3:
                        users.append({"username": r[0], "password": r[1], "role": r[2]})
            return users
        except Exception:
            return []

    def login_user(self):
        uname = (self.login_username.get() or "").strip()
        pwd = (self.login_password.get() or "").strip()
        if not uname or not pwd:
            messagebox.showerror("Login failed", "Enter username and password.")
            return

        users = self._read_users()
        for u in users:
            if u["username"] == uname and u["password"] == pwd:
                self.current_user = {"username": uname, "role": (u.get("role") or "student")}
                role = self.current_user["role"].lower()
                if role == "admin":
                    self.create_admin_home()
                else:
                    self.create_student_home()
                return

        messagebox.showerror("Login failed", "Invalid username or password.")

    def register_user(self):
        uname = (self.signup_username.get() or "").strip()
        pwd = (self.signup_password.get() or "").strip()
        role = (self.signup_role.get() or "").strip().lower()
        if not uname or not pwd or role not in ("admin", "student"):
            messagebox.showerror("Error", "Enter username, password and role (admin or student).")
            return

        users = self._read_users()
        for u in users:
            if u["username"] == uname:
                messagebox.showerror("Error", "Username already exists.")
                return

        with open(USER_FILE, "a", newline="") as f:
            csv.writer(f).writerow([uname, pwd, role])
        messagebox.showinfo("Success", "Account created. You can log in.")
        self.create_login_page()

    # ---------- admin / student homes ----------
    def create_admin_home(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.set_background(self.root, "admin_bg.png")

        tk.Label(self.root, text=f"Admin Dashboard ( {self.current_user['username']} )",
                 font=("Arial", 22, "bold"), bg="white").pack(pady=12)
        btn_frame = tk.Frame(self.root, bg="white")
        btn_frame.place(relx=0.5, rely=0.55, anchor="center")

        tk.Button(btn_frame, text="Manage Courses", width=28, font=("Arial", 13), command=self.manage_courses_page).grid(row=0, column=0, pady=6)
        tk.Button(btn_frame, text="Add / Update Student Grade", width=28, font=("Arial", 13), command=self.add_student_grade_page).grid(row=1, column=0, pady=6)
        tk.Button(btn_frame, text="Edit / Delete Student Records", width=28, font=("Arial", 13), command=self.edit_delete_page).grid(row=2, column=0, pady=6)
        tk.Button(btn_frame, text="Generate Student Report (by ID)", width=28, font=("Arial", 13), command=self.generate_report_page).grid(row=3, column=0, pady=6)
        tk.Button(btn_frame, text="All Students Report (table)", width=28, font=("Arial", 13), command=self.all_students_report).grid(row=4, column=0, pady=6)
        tk.Button(btn_frame, text="Logout", width=28, font=("Arial", 13), command=self.logout).grid(row=5, column=0, pady=6)

    def create_student_home(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.set_background(self.root, "student_bg.png")

        tk.Label(self.root, text=f"Student Dashboard ( {self.current_user['username']} )",
                 font=("Arial", 22, "bold"), bg="white").pack(pady=12)
        frame = tk.Frame(self.root, bg="white")
        frame.place(relx=0.5, rely=0.55, anchor="center")

        tk.Button(frame, text="View My Performance Report", width=28, font=("Arial", 13), command=self.student_view_own_report).pack(pady=8)
        tk.Button(frame, text="Logout", width=28, font=("Arial", 13), command=self.logout).pack(pady=8)

    def logout(self):
        self.current_user = None
        self.create_login_page()

    # ---------- course mgmt ----------
    def manage_courses_page(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.set_background(self.root, "courses_bg.png")

        tk.Label(self.root, text="Manage Courses", font=("Arial", 20, "bold"), bg="white").pack(pady=8)
        frame = tk.Frame(self.root, bg="white")
        frame.place(relx=0.5, rely=0.55, anchor="center")

        tk.Label(frame, text="Course Code", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=6, pady=4)
        self.course_code_e = tk.Entry(frame, font=("Arial", 12))
        self.course_code_e.grid(row=0, column=1, padx=6, pady=4)

        tk.Label(frame, text="Course Name", font=("Arial", 12), bg="white").grid(row=1, column=0, padx=6, pady=4)
        self.course_name_e = tk.Entry(frame, width=35, font=("Arial", 12))
        self.course_name_e.grid(row=1, column=1, padx=6, pady=4)

        btn_frame = tk.Frame(self.root, bg="white")
        btn_frame.pack(pady=6)
        
        # existing courses list
        list_frame = tk.Frame(self.root, bg="white")
        list_frame.place(relx=0.5, rely=0.25, anchor="n")
        tk.Label(list_frame, text="Existing courses:", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        courses_box = tk.Text(list_frame, height=8, width=80, font=("Arial", 11))
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
        
        tk.Button(btn_frame, text="Add Course", font=("Arial", 12), command=self.add_course).grid(row=2, column=0, padx=6,pady=8)
        tk.Button(btn_frame, text="Back", font=("Arial", 12), command=self.create_admin_home).grid(row=2, column=1, padx=6,pady=8)


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

    # ---------- add/update student grade ----------
    def add_student_grade_page(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.set_background(self.root, "report_bg.png")

        tk.Label(self.root, text="Add / Update Student Grade", font=("Arial", 18, "bold"), bg="white").pack(pady=8)
        frame = tk.Frame(self.root, bg="white")
        frame.place(relx=0.5, rely=0.55, anchor="center")

        tk.Label(frame, text="Student ID", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=6, pady=4)
        self.as_sid = tk.Entry(frame, font=("Arial", 12))
        self.as_sid.grid(row=0, column=1, padx=6, pady=4)

        tk.Label(frame, text="Student Name", font=("Arial", 12), bg="white").grid(row=1, column=0, padx=6, pady=4)
        self.as_name = tk.Entry(frame, font=("Arial", 12))
        self.as_name.grid(row=1, column=1, padx=6, pady=4)

        tk.Label(frame, text="Course Code", font=("Arial", 12), bg="white").grid(row=2, column=0, padx=6, pady=4)
        self.as_course = tk.Entry(frame, font=("Arial", 12))
        self.as_course.grid(row=2, column=1, padx=6, pady=4)

        tk.Label(frame, text="Marks", font=("Arial", 12), bg="white").grid(row=3, column=0, padx=6, pady=4)
        self.as_marks = tk.Entry(frame, font=("Arial", 12))
        self.as_marks.grid(row=3, column=1, padx=6, pady=4)

        btn_frame = tk.Frame(self.root, bg="white")
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Save / Update", font=("Arial", 12), command=self.save_student_grade).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Back", font=("Arial", 12), command=self.create_admin_home).grid(row=0, column=1, padx=6)

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
                if r and len(r) >= 1 and r[0] == course:
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

        # ensure header exists
        if not rows:
            rows = [["ID", "Name", "CourseCode", "Marks", "Grade"]]

        for i, row in enumerate(rows):
            if i == 0:
                continue
            if row and len(row) >= 3 and row[0] == sid and row[2] == course:
                rows[i] = [sid, name, course, f"{marks:.2f}", grade]
                updated = True

        if updated:
            with open(STUDENT_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            messagebox.showinfo("Updated", f"Updated marks for {sid} - {course}.")
        else:
            with open(STUDENT_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([sid, name, course, f"{marks:.2f}", grade])
            messagebox.showinfo("Saved", f"Saved record for {sid} - {course}.")

        # clear inputs
        self.as_sid.delete(0, tk.END)
        self.as_name.delete(0, tk.END)
        self.as_course.delete(0, tk.END)
        self.as_marks.delete(0, tk.END)

    # ---------- edit/delete student records ----------
    def edit_delete_page(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.set_background(self.root, "report_bg.png")

        tk.Label(self.root, text="Edit / Delete Student Records", font=("Arial", 18, "bold"), bg="white").pack(pady=8)
        frame = tk.Frame(self.root, bg="white")
        frame.place(relx=0.5, rely=0.55, anchor="center")

        tk.Label(frame, text="Enter Student ID", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=6, pady=4)
        self.ed_search_id = tk.Entry(frame, font=("Arial", 12))
        self.ed_search_id.grid(row=0, column=1, padx=6, pady=4)
        tk.Button(frame, text="Search", font=("Arial", 12), command=self.search_student_records).grid(row=0, column=2, padx=6)
        tk.Button(frame, text="Back", font=("Arial", 12), command=self.create_admin_home).grid(row=1, column=1, pady=8)

    def search_student_records(self):
        sid = (self.ed_search_id.get() or "").strip()
        if not sid:
            messagebox.showerror("Input error", "Enter student ID.")
            return

        with open(STUDENT_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            records = [r for r in reader if r and len(r) >= 1 and r[0] == sid]

        if not records:
            messagebox.showerror("Not found", "No records for this student ID.")
            return

        win = tk.Toplevel(self.root)
        win.title(f"Records for {sid}")
        tk.Label(win, text=f"Student ID: {sid}  |  Name: {records[0][1] if len(records[0])>1 else ''}", font=("Arial", 14, "bold")).pack(pady=8)

        for rec in records:
            frame = tk.Frame(win, pady=4)
            frame.pack(fill="x", padx=8)
            lbl_text = f"{rec[2]}  -  Marks: {rec[3]}  |  Grade: {rec[4]}" if len(rec) >=5 else str(rec)
            lbl = tk.Label(frame, text=lbl_text, anchor="w")
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
        new_marks_e.insert(0, record[3] if len(record) > 3 else "")

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
                if i == 0:
                    continue
                if r and len(r) >= 3 and r[0] == record[0] and r[2] == record[2]:
                    # ensure row has 5 cols
                    while len(r) < 5:
                        r.append("")
                    rows[i][3] = f"{nm:.2f}"
                    rows[i][4] = new_grade
            with open(STUDENT_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            messagebox.showinfo("Saved", "Marks updated.")
            ew.destroy()
            parent_win.destroy()

        tk.Button(ew, text="Save", font=("Arial", 12), command=save_edit).pack(pady=6)

    def delete_course_record(self, record, parent_win):
        with open(STUDENT_FILE, "r", newline="") as f:
            rows = list(csv.reader(f))
        new_rows = [r for r in rows if not (r and len(r) >= 3 and r[0] == record[0] and r[2] == record[2])]
        with open(STUDENT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(new_rows)
        messagebox.showinfo("Deleted", f"Deleted {record[2]} for {record[0]}.")
        parent_win.destroy()

    # ---------- reports ----------
    def generate_report_page(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.set_background(self.root, "report_bg.png")

        tk.Label(self.root, text="Generate Student Report (by ID)", font=("Arial", 18, "bold"), bg="white").pack(pady=8)
        frame = tk.Frame(self.root, bg="white")
        frame.place(relx=0.5, rely=0.55, anchor="center")

        tk.Label(frame, text="Student ID", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=6)
        self.rp_student_id = tk.Entry(frame, font=("Arial", 12))
        self.rp_student_id.grid(row=0, column=1, padx=6)
        tk.Button(frame, text="Generate", font=("Arial", 12), command=self.generate_student_report_by_id).grid(row=0, column=2, padx=6)
        tk.Button(self.root, text="Back", font=("Arial", 12), command=self.create_admin_home).pack(pady=8)

    def generate_student_report_by_id(self):
        sid = (self.rp_student_id.get() or "").strip()
        if not sid:
            messagebox.showerror("Input", "Enter student ID.")
            return
        with open(STUDENT_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            recs = [r for r in reader if r and len(r) >= 1 and r[0] == sid]
        if not recs:
            messagebox.showerror("Not found", "No records for this ID.")
            return
        self.show_student_report(recs)

    def student_view_own_report(self):
        sid_or_name = (self.current_user.get("username") or "").strip()
        # try to find by ID first, then by Name
        with open(STUDENT_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            recs_by_id = [r for r in reader if r and len(r) >=1 and r[0] == sid_or_name]
            f.seek(0); next(reader, None)  # reset and skip header used above (we re-open instead)
        if recs_by_id:
            self.show_student_report(recs_by_id)
            return

        # fallback: search by Name (case-insensitive)
        with open(STUDENT_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            recs_by_name = [r for r in reader if r and len(r) >=2 and r[1].lower() == sid_or_name.lower()]
        if recs_by_name:
            self.show_student_report(recs_by_name)
            return

        messagebox.showerror("No records", "No records found for your ID or name.")

    def show_student_report(self, recs):
        # recs: list of [ID, Name, CourseCode, Marks, Grade]
        win = tk.Toplevel(self.root)
        win.title(f"Performance Report - {recs[0][1] if len(recs[0])>1 else recs[0][0]} ({recs[0][0]})")
        win.geometry("850x700")

        tk.Label(win, text=f"{recs[0][1]}  —  {recs[0][0]}", font=("Arial", 16, "bold")).pack(pady=8)

        list_frame = tk.Frame(win)
        list_frame.pack(pady=6)
        tk.Label(list_frame, text="Course - Marks - Grade", font=("Arial", 12, "bold")).pack(anchor="w")
        for r in recs:
            # make robust display even if malformed row
            course = r[2] if len(r) > 2 else "(unknown)"
            marks = r[3] if len(r) > 3 else "0"
            grade = r[4] if len(r) > 4 else "F"
            tk.Label(list_frame, text=f"{course}  |  Marks: {marks}  |  Grade: {grade}", anchor="w").pack(anchor="w")

        # marks and grades arrays (guarded)
        marks = []
        grades = []
        for r in recs:
            try:
                marks.append(float(r[3]))
            except Exception:
                marks.append(0.0)
            try:
                grades.append(r[4])
            except Exception:
                grades.append("F")

        avg_marks = sum(marks) / len(marks) if marks else 0.0
        highest = max(marks) if marks else 0.0
        lowest = min(marks) if marks else 0.0
        gpa = self.compute_gpa_for_records(recs)

        stats_frame = tk.Frame(win)
        stats_frame.pack(pady=8)
        tk.Label(stats_frame, text=f"Average Marks: {avg_marks:.2f}", font=("Arial", 12)).grid(row=0, column=0, padx=8, pady=4)
        tk.Label(stats_frame, text=f"Highest: {highest:.2f}", font=("Arial", 12)).grid(row=0, column=1, padx=8, pady=4)
        tk.Label(stats_frame, text=f"Lowest: {lowest:.2f}", font=("Arial", 12)).grid(row=0, column=2, padx=8, pady=4)
        tk.Label(stats_frame, text=f"GPA: {gpa:.2f}", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=8, pady=4)

        subjects = [r[2] if len(r)>2 else "(unknown)" for r in recs]
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(marks if marks else [1], labels=subjects, autopct="%1.1f%%", startangle=90)
        ax.set_title("Subject-wise Marks Distribution")
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        tk.Button(win, text="Close", font=("Arial", 12), command=win.destroy).pack(pady=6)

    # ---------- all students report (table) ----------
    def all_students_report(self):
        # aggregate per student
        students = {}
        with open(STUDENT_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for r in reader:
                if not r or len(r) < 5:
                    continue
                sid, name, course, marks_s, grade = r[0], r[1], r[2], r[3], r[4]
                try:
                    marks = float(marks_s)
                except:
                    marks = 0.0
                if sid not in students:
                    students[sid] = {"name": name, "marks": [], "grades": []}
                students[sid]["marks"].append(marks)
                students[sid]["grades"].append(grade)

        win = tk.Toplevel(self.root)
        win.title("All Students Report")
        win.geometry("900x600")
        win.configure(bg='#032036')
        tk.Label(win, text="All Students Report",bg='#032036',fg='white',font=("Arial", 16, "bold")).pack(pady=8)

        cols = ("Student ID", "Name", "Courses Count", "Avg Marks", "GPA")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=18)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=160, anchor="center")
        tree.pack(pady=8, fill="both", expand=True)

        for sid, info in students.items():
            avg_marks = sum(info["marks"]) / len(info["marks"]) if info["marks"] else 0.0
            gpa = self.compute_gpa_for_grade_list(info["grades"])
            tree.insert("", tk.END, values=(sid, info["name"], len(info["marks"]), f"{avg_marks:.2f}", f"{gpa:.2f}"))

        btnf = tk.Frame(win)
        btnf.pack(pady=8)
        tk.Button(btnf, text="Close",bg='#990516',fg='white', font=("Arial", 12), command=win.destroy).pack()

    # ---------- grading & gpa helpers ----------
    def marks_to_grade(self, marks: float) -> str:
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
        mapping = {"S": 5.0, "A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}
        return mapping.get((grade or "").upper(), 0.0)

    def compute_gpa_for_records(self, recs) -> float:
        points = []
        for r in recs:
            try:
                g = r[4]
            except Exception:
                g = "F"
            points.append(self.grade_to_gpa_point(g))
        if not points:
            return 0.0
        return sum(points) / len(points)

    def compute_gpa_for_grade_list(self, grade_list) -> float:
        points = [self.grade_to_gpa_point(g) for g in grade_list]
        if not points:
            return 0.0
        return sum(points) / len(points)

# ---------- main ----------
def main():
    root = tk.Tk()
    app = GradeTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

