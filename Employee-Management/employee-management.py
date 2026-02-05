import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

# ================= DATABASE FILES =================
EMP_FILE = "employees.db"
ATT_FILE = "attendance.db"
LEAVE_FILE = "leaves.db"
PAY_FILE = "payroll.db"
APP_FILE = "appraisal.db"

# ================= DATABASE UTILITIES =================
def read_db(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return [line.strip().split("|") for line in f]

def write_db(file, data):
    with open(file, "w") as f:
        for row in data:
            f.write("|".join(row) + "\n")

# ================= EMPLOYEE MODULE =================
def add_employee():
    emp = [
        emp_id.get(), emp_name.get(), emp_age.get(),
        emp_gender.get(), emp_dept.get(), emp_role.get(),
        emp_salary.get(), "Active",
        datetime.now().strftime("%d-%m-%Y")
    ]
    if "" in emp:
        messagebox.showerror("Error", "All fields required")
        return

    data = read_db(EMP_FILE)
    if any(e[0] == emp[0] for e in data):
        messagebox.showerror("Error", "Employee ID exists")
        return

    data.append(emp)
    write_db(EMP_FILE, data)
    refresh_employees()

def refresh_employees():
    emp_table.delete(*emp_table.get_children())
    for e in read_db(EMP_FILE):
        emp_table.insert("", "end", values=e)

# ================= ATTENDANCE MODULE =================
def mark_attendance(status):
    if emp_id.get() == "":
        messagebox.showerror("Error", "Enter Employee ID")
        return
    record = [
        emp_id.get(),
        datetime.now().strftime("%d-%m-%Y"),
        status
    ]
    data = read_db(ATT_FILE)
    data.append(record)
    write_db(ATT_FILE, data)
    messagebox.showinfo("Saved", f"{status} marked")

def get_present_days(eid):
    return sum(1 for a in read_db(ATT_FILE) if a[0] == eid and a[2] == "Present")

# ================= LEAVE MODULE =================
def apply_leave():
    record = [
        emp_id.get(),
        leave_type.get(),
        leave_days.get(),
        "Approved"
    ]
    data = read_db(LEAVE_FILE)
    data.append(record)
    write_db(LEAVE_FILE, data)
    messagebox.showinfo("Leave", "Leave Approved")

# ================= PAYROLL MODULE =================
def generate_salary():
    eid = emp_id.get()
    emp = next((e for e in read_db(EMP_FILE) if e[0] == eid), None)
    if not emp:
        messagebox.showerror("Error", "Employee not found")
        return

    basic = int(emp[6])
    present = get_present_days(eid)

    hra = basic * 0.20
    da = basic * 0.10
    gross = basic + hra + da
    net = int((gross / 30) * present)

    record = [
        eid, str(basic), str(int(hra)), str(int(da)),
        str(present), str(net)
    ]
    data = read_db(PAY_FILE)
    data.append(record)
    write_db(PAY_FILE, data)

    salary_output.config(
        text=f"Present: {present} | Net Salary: ₹{net}"
    )

# ================= APPRAISAL MODULE =================
def apply_appraisal():
    record = [
        emp_id.get(),
        rating.get(),
        increment.get(),
        datetime.now().strftime("%Y")
    ]
    data = read_db(APP_FILE)
    data.append(record)
    write_db(APP_FILE, data)
    messagebox.showinfo("Appraisal", "Appraisal Recorded")

# ================= GUI =================
root = tk.Tk()
root.title("Enterprise Employee ERP System")
root.geometry("1350x780")
root.configure(bg="#f4f6f9")

style = ttk.Style()
style.theme_use("default")

# ----------- GLOBAL STYLES -----------
style.configure("TLabel", background="#f4f6f9", font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"))
style.configure("Section.TLabelframe", background="#ffffff")
style.configure("Section.TLabelframe.Label", font=("Segoe UI", 12, "bold"))
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("Treeview",
                font=("Segoe UI", 10),
                rowheight=28)
style.configure("Treeview.Heading",
                font=("Segoe UI", 10, "bold"))

# ================= HEADER =================
header = tk.Frame(root, bg="#1f2937", height=70)
header.pack(fill="x")

tk.Label(
    header,
    text="Enterprise Employee Management ERP",
    fg="white",
    bg="#1f2937",
    font=("Segoe UI", 22, "bold")
).pack(pady=15)

# ================= MAIN CONTAINER =================
main = tk.Frame(root, bg="#f4f6f9")
main.pack(fill="both", expand=True, padx=15, pady=10)

# ================= EMPLOYEE FORM =================
form = ttk.Labelframe(main, text="Employee Master", style="Section.TLabelframe")
form.pack(fill="x", pady=10)

labels = ["Employee ID", "Name", "Age", "Gender", "Department", "Role", "Basic Salary"]
entries = []

for i, label in enumerate(labels):
    ttk.Label(form, text=label).grid(row=0, column=i, padx=8, pady=5)
    entry = ttk.Entry(form, width=18)
    entry.grid(row=1, column=i, padx=8, pady=5)
    entries.append(entry)

emp_id, emp_name, emp_age, emp_gender, emp_dept, emp_role, emp_salary = entries

ttk.Button(form, text="➕ Add Employee", command=add_employee)\
    .grid(row=2, column=0, pady=10)

# ================= ATTENDANCE =================
att = ttk.Labelframe(main, text="Attendance", style="Section.TLabelframe")
att.pack(fill="x", pady=10)

ttk.Button(att, text="✔ Present",
           command=lambda: mark_attendance("Present")).pack(side="left", padx=8)
ttk.Button(att, text="✖ Absent",
           command=lambda: mark_attendance("Absent")).pack(side="left", padx=8)
ttk.Button(att, text="🏖 Leave",
           command=lambda: mark_attendance("Leave")).pack(side="left", padx=8)

# ================= PAYROLL =================
pay = ttk.Labelframe(main, text="Payroll", style="Section.TLabelframe")
pay.pack(fill="x", pady=10)

ttk.Button(pay, text="💰 Generate Salary", command=generate_salary)\
    .pack(side="left", padx=10)

salary_output = ttk.Label(
    pay,
    text="Present: 0 | Net Salary: ₹0",
    font=("Segoe UI", 12, "bold")
)
salary_output.pack(side="left", padx=20)

# ================= APPRAISAL =================
app = ttk.Labelframe(main, text="Performance Appraisal", style="Section.TLabelframe")
app.pack(fill="x", pady=10)

ttk.Label(app, text="Rating").pack(side="left", padx=5)
rating = ttk.Entry(app, width=10)
rating.pack(side="left", padx=5)

ttk.Label(app, text="Increment %").pack(side="left", padx=5)
increment = ttk.Entry(app, width=10)
increment.pack(side="left", padx=5)

ttk.Button(app, text="Apply Appraisal", command=apply_appraisal)\
    .pack(side="left", padx=10)

# ================= EMPLOYEE TABLE =================
table_frame = ttk.Labelframe(main, text="Employee Records", style="Section.TLabelframe")
table_frame.pack(fill="both", expand=True, pady=10)

cols = ["ID","Name","Age","Gender","Dept","Role","Salary","Status","Join Date"]
emp_table = ttk.Treeview(table_frame, columns=cols, show="headings")

for col in cols:
    emp_table.heading(col, text=col)
    emp_table.column(col, anchor="center", width=140)

emp_table.pack(fill="both", expand=True, padx=10, pady=10)

refresh_employees()
root.mainloop()
