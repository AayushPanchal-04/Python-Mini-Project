import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime

# ================== APP CONFIG ==================
APP_TITLE = "Smart Health Analyzer Pro"
WINDOW_SIZE = "1000x600"
FILE_NAME = "health_history.csv"

# ================== MAIN WINDOW ==================
root = tk.Tk()
root.title(APP_TITLE)
root.geometry(WINDOW_SIZE)
root.resizable(False, False)

# ================== THEME ==================
style = ttk.Style()
style.theme_use("clam")

LIGHT_BG = "#f4f6f8"
DARK_BG = "#1e1e1e"
CARD_BG = "#ffffff"
PRIMARY = "#2563eb"

is_dark = False

def apply_theme():
    bg = DARK_BG if is_dark else LIGHT_BG
    card = "#2a2a2a" if is_dark else CARD_BG
    fg = "white" if is_dark else "black"

    root.configure(bg=bg)
    style.configure("TFrame", background=bg)
    style.configure("Card.TFrame", background=card)
    style.configure("TLabel", background=card, foreground=fg)
    style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"))
    style.configure("Value.TLabel", font=("Segoe UI", 16, "bold"), foreground=PRIMARY)
    style.configure("TButton", font=("Segoe UI", 11, "bold"))

apply_theme()

# ================== FUNCTIONS ==================
def analyze_health():
    try:
        name = name_entry.get()
        age = int(age_entry.get())
        gender = gender_var.get()
        height = float(height_entry.get())
        weight = float(weight_entry.get())

        if not name or gender == "Select":
            raise ValueError

        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 2)

        if bmi < 18.5:
            status = "Underweight"
            advice = "Increase calorie intake"
        elif bmi < 25:
            status = "Normal"
            advice = "Maintain healthy lifestyle"
        elif bmi < 30:
            status = "Overweight"
            advice = "Regular exercise recommended"
        else:
            status = "Obese"
            advice = "Medical guidance suggested"

        bmr = round(
            (88.36 + 13.4 * weight + 4.8 * height - 5.7 * age)
            if gender == "Male"
            else (447.6 + 9.2 * weight + 3.1 * height - 4.3 * age), 2
        )

        ideal_weight = round(22 * (height_m ** 2), 2)
        body_fat = round((1.20 * bmi) + (0.23 * age) - (16.2 if gender == "Male" else 5.4), 2)

        bmi_value.config(text=bmi)
        bmi_status.config(text=status)
        bmr_value.config(text=f"{bmr} kcal/day")
        ideal_value.config(text=f"{ideal_weight} kg")
        fat_value.config(text=f"{body_fat} %")
        advice_value.config(text=advice)

        save_history(name, bmi, status, bmr, ideal_weight)

    except:
        messagebox.showerror("Invalid Input", "Please enter correct details")

def save_history(name, bmi, status, bmr, ideal):
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%d-%m-%Y %H:%M"),
            name, bmi, status, bmr, ideal
        ])
    load_history()

def load_history():
    history_table.delete(*history_table.get_children())
    try:
        with open(FILE_NAME, "r") as file:
            for row in csv.reader(file):
                history_table.insert("", "end", values=row)
    except:
        pass

def toggle_theme():
    global is_dark
    is_dark = not is_dark
    apply_theme()

# ================== SIDEBAR ==================
sidebar = ttk.Frame(root, width=200)
sidebar.pack(side="left", fill="y")

ttk.Label(sidebar, text="Health Pro", style="Header.TLabel").pack(pady=20)
ttk.Button(sidebar, text="Toggle Theme", command=toggle_theme).pack(pady=10)

# ================== MAIN AREA ==================
main = ttk.Frame(root)
main.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# ================== USER CARD ==================
user_card = ttk.Frame(main, style="Card.TFrame", padding=20)
user_card.pack(fill="x", pady=10)

ttk.Label(user_card, text="User Profile", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=10)

name_entry = ttk.Entry(user_card)
age_entry = ttk.Entry(user_card)
height_entry = ttk.Entry(user_card)
weight_entry = ttk.Entry(user_card)

gender_var = tk.StringVar(value="Select")
gender_box = ttk.Combobox(user_card, textvariable=gender_var, values=["Male", "Female"], state="readonly")

labels = ["Name", "Age", "Gender", "Height (cm)", "Weight (kg)"]
widgets = [name_entry, age_entry, gender_box, height_entry, weight_entry]

for i, (lbl, w) in enumerate(zip(labels, widgets)):
    ttk.Label(user_card, text=lbl).grid(row=i+1, column=0, sticky="w", pady=5)
    w.grid(row=i+1, column=1, pady=5, sticky="ew")

ttk.Button(user_card, text="Analyze Health", command=analyze_health).grid(row=7, column=0, columnspan=2, pady=15)

# ================== RESULTS ==================
result_card = ttk.Frame(main, style="Card.TFrame", padding=20)
result_card.pack(fill="x", pady=10)

bmi_value = ttk.Label(result_card, text="--", style="Value.TLabel")
bmi_status = ttk.Label(result_card, text="--")
bmr_value = ttk.Label(result_card, text="--")
ideal_value = ttk.Label(result_card, text="--")
fat_value = ttk.Label(result_card, text="--")
advice_value = ttk.Label(result_card, text="--")

results = [
    ("BMI", bmi_value),
    ("Status", bmi_status),
    ("BMR", bmr_value),
    ("Ideal Weight", ideal_value),
    ("Body Fat %", fat_value),
    ("Health Advice", advice_value),
]

for i, (lbl, val) in enumerate(results):
    ttk.Label(result_card, text=lbl).grid(row=i, column=0, sticky="w", pady=3)
    val.grid(row=i, column=1, sticky="w")

# ================== HISTORY ==================
history_card = ttk.Frame(main, style="Card.TFrame", padding=15)
history_card.pack(fill="both", expand=True)

columns = ("Date", "Name", "BMI", "Status", "BMR", "Ideal")
history_table = ttk.Treeview(history_card, columns=columns, show="headings")
for c in columns:
    history_table.heading(c, text=c)
    history_table.column(c, width=120)

history_table.pack(fill="both", expand=True)
load_history()

# ================== RUN ==================
root.mainloop()
