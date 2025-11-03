import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ===== DATABASE CONNECTION =====
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",       
            password="root",   
            database="grade_system"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to database:\n{err}")
        raise SystemExit

# ===== MAIN WINDOW =====
root = tk.Tk()
root.title("Student Grade Tracking System")
root.geometry("800x500")
root.resizable(False, False)

# ===== LOGIN WINDOW =====
def show_login():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="STUDENT GRADE TRACKING SYSTEM", font=("Arial", 18, "bold")).pack(pady=30)
    tk.Label(root, text="Login", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT role FROM users WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        db.close()

        if result:
            role = result[0]
            if role == "admin":
                show_admin_dashboard()
            else:
                show_student_dashboard(username)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    tk.Button(root, text="Login", bg="green", fg="white", width=15, command=login).pack(pady=15)
    tk.Button(root, text="Don't have an account? Sign Up", fg="blue", command=show_signup).pack()

# ===== SIGNUP WINDOW =====
def show_signup():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="CREATE AN ACCOUNT", font=("Arial", 18, "bold")).pack(pady=30)

    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    tk.Label(root, text="Role (admin/student)").pack()
    role_var = tk.StringVar(value="student")
    role_box = ttk.Combobox(root, textvariable=role_var, values=["admin", "student"], state="readonly", width=15)
    role_box.pack(pady=5)

    def signup():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        role = role_var.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        db = connect_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, password, role)
            )
            db.commit()
            messagebox.showinfo("Success", "Account created successfully! You can now log in.")
            show_login()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        finally:
            db.close()

    tk.Button(root, text="Sign Up", bg="green", fg="white", width=15, command=signup).pack(pady=15)
    tk.Button(root, text="Back to Login", fg="blue", command=show_login).pack()

# ===== ADMIN DASHBOARD =====
def show_admin_dashboard():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="ADMIN DASHBOARD", font=("Arial", 16, "bold")).pack(pady=10)
    
    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Label(frame, text="Student").grid(row=0, column=0, padx=5)
    student_entry = tk.Entry(frame)
    student_entry.grid(row=0, column=1, padx=5)

    tk.Label(frame, text="Subject").grid(row=0, column=2, padx=5)
    subject_entry = tk.Entry(frame)
    subject_entry.grid(row=0, column=3, padx=5)

    tk.Label(frame, text="Marks").grid(row=0, column=4, padx=5)
    marks_entry = tk.Entry(frame)
    marks_entry.grid(row=0, column=5, padx=5)

    # Add Marks
    def add_marks():
        student = student_entry.get().strip()
        subject = subject_entry.get().strip()
        marks = marks_entry.get().strip()

        if not (student and subject and marks.isdigit()):
            messagebox.showerror("Error", "Please fill all fields correctly!")
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO marks (student, subject, marks) VALUES (%s, %s, %s)",
                       (student, subject, marks))
        db.commit()
        db.close()
        messagebox.showinfo("Success", "Marks added successfully!")
        load_data()
        student_entry.delete(0, tk.END)
        subject_entry.delete(0, tk.END)
        marks_entry.delete(0, tk.END)

    tk.Button(frame, text="Add Marks", command=add_marks, bg="green", fg="white").grid(row=0, column=6, padx=5)

    # Table
    tree = ttk.Treeview(root, columns=("ID", "Student", "Subject", "Marks"), show='headings')
    for col in ("ID", "Student", "Subject", "Marks"):
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")
    tree.pack(pady=20, fill='both', expand=True)

    # Load Data
    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM marks ORDER BY id ASC")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        db.close()

    # Delete Record
    def delete_record():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a record to delete!")
            return
        record = tree.item(selected[0])['values']
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM marks WHERE id=%s", (record[0],))
        db.commit()
        db.close()
        messagebox.showinfo("Deleted", "Record deleted successfully!")
        load_data()

    # Edit Record
    def edit_record():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a record to edit!")
            return
        record = tree.item(selected[0])['values']

        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Record")
        edit_window.geometry("300x250")
        edit_window.resizable(False, False)

        tk.Label(edit_window, text="Subject").pack(pady=5)
        sub_entry = tk.Entry(edit_window)
        sub_entry.insert(0, record[2])
        sub_entry.pack()

        tk.Label(edit_window, text="Marks").pack(pady=5)
        mark_entry = tk.Entry(edit_window)
        mark_entry.insert(0, record[3])
        mark_entry.pack()

        def update_record():
            new_subject = sub_entry.get().strip()
            new_marks = mark_entry.get().strip()

            if not (new_subject and new_marks.isdigit()):
                messagebox.showerror("Error", "Invalid input!")
                return

            db = connect_db()
            cursor = db.cursor()
            cursor.execute("UPDATE marks SET subject=%s, marks=%s WHERE id=%s",
                           (new_subject, new_marks, record[0]))
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Record updated successfully!")
            edit_window.destroy()
            load_data()

        tk.Button(edit_window, text="Save Changes", bg="blue", fg="white", command=update_record).pack(pady=10)

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Edit Record", command=edit_record, bg="orange", fg="white", width=15).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Delete Record", command=delete_record, bg="red", fg="white", width=15).grid(row=0, column=1, padx=10)
    tk.Button(button_frame, text="Logout", command=show_login, bg="gray", fg="white", width=15).grid(row=0, column=2, padx=10)

    load_data()

# ===== STUDENT DASHBOARD =====
def show_student_dashboard(username):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"STUDENT DASHBOARD - {username}", font=("Arial", 16, "bold")).pack(pady=10)

    tree = ttk.Treeview(root, columns=("ID", "Subject", "Marks"), show='headings')
    for col in ("ID", "Subject", "Marks"):
        tree.heading(col, text=col)
        tree.column(col, width=200, anchor="center")
    tree.pack(pady=20, fill='both', expand=True)

    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, subject, marks FROM marks WHERE student=%s ORDER BY id ASC", (username,))
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        db.close()

    tk.Button(root, text="Logout", command=show_login, bg="gray", fg="white", width=15).pack(pady=10)
    load_data()

# ===== START APP =====
show_login()
root.mainloop()
