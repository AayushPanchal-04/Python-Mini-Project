import tkinter as tk
from tkinter import Frame, Canvas
from datetime import datetime

# -------------------- Logic --------------------

def get_bot_response(user_msg):
    user_msg = user_msg.lower()

    if any(x in user_msg for x in ["hi", "hello", "hey"]):
        return "Hello 👋 How can I help you today?"

    if "college" in user_msg:
        return "I can help with college information, courses, and FAQs."

    if "office" in user_msg:
        return "I assist with office and workplace-related queries."

    if "time" in user_msg:
        return datetime.now().strftime("Current time: %H:%M:%S")

    if "date" in user_msg:
        return datetime.now().strftime("Today's date: %d-%m-%Y")

    if "bye" in user_msg:
        return "Goodbye 👋 Have a great day!"

    return "I'm still learning 🤖 Please try a different question."

# -------------------- Message Bubble --------------------

def add_message(text, sender="bot"):
    bubble = Frame(chat_frame, bg=BG)

    color = USER_BUBBLE if sender == "user" else BOT_BUBBLE
    fg = "white" if sender == "user" else "#e5e7eb"
    anchor = "e" if sender == "user" else "w"

    msg = tk.Label(
        bubble,
        text=text,
        bg=color,
        fg=fg,
        font=("Segoe UI", 10),
        wraplength=320,
        padx=14,
        pady=10,
        justify="left"
    )

    msg.pack(anchor=anchor)
    bubble.pack(anchor=anchor, pady=6, padx=14)

    canvas.update_idletasks()
    canvas.yview_moveto(1)

def send_message(event=None):
    text = user_entry.get().strip()
    if not text:
        return

    landing_frame.pack_forget()
    add_message(text, "user")
    user_entry.delete(0, tk.END)

    root.after(500, lambda: add_message(get_bot_response(text), "bot"))

# -------------------- Colors --------------------

BG = "#0b0f14"
HEADER = "#111827"
BOT_BUBBLE = "#1f2937"
USER_BUBBLE = "#2563eb"
INPUT_BG = "#111827"

# -------------------- Window --------------------

root = tk.Tk()
root.title("AI Chat")
root.geometry("520x640")
root.configure(bg=BG)
root.resizable(False, False)

# -------------------- Header --------------------

header = Frame(root, bg=HEADER, height=55)
header.pack(fill="x")

tk.Label(
    header,
    text="✨  AI Chat",
    bg=HEADER,
    fg="white",
    font=("Segoe UI", 14, "bold")
).pack(side="left", padx=15, pady=12)

# -------------------- Chat Area --------------------

chat_container = Frame(root, bg=BG)
chat_container.pack(fill="both", expand=True)

canvas = Canvas(chat_container, bg=BG, highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

chat_frame = Frame(canvas, bg=BG)
canvas.create_window((0, 0), window=chat_frame, anchor="nw")

chat_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# -------------------- Landing Screen --------------------

landing_frame = Frame(chat_frame, bg=BG)
landing_frame.pack(expand=True, pady=120)

tk.Label(
    landing_frame,
    text="What can I help you with?",
    bg=BG,
    fg="white",
    font=("Segoe UI", 18, "bold")
).pack(pady=25)

def suggestion(text):
    return tk.Button(
        landing_frame,
        text=text,
        font=("Segoe UI", 10),
        bg=BOT_BUBBLE,
        fg="white",
        relief="flat",
        padx=16,
        pady=8,
        command=lambda: [user_entry.insert(0, text), send_message()]
    )

row1 = Frame(landing_frame, bg=BG)
row1.pack(pady=8)

suggestion("✔ College Help").pack(in_=row1, side="left", padx=8)
suggestion("📍 Office Support").pack(in_=row1, side="left", padx=8)

row2 = Frame(landing_frame, bg=BG)
row2.pack(pady=8)

suggestion("⚙ System Time").pack(in_=row2, side="left", padx=8)
suggestion("⭐ What can you do?").pack(in_=row2, side="left", padx=8)

# -------------------- Input Bar --------------------

input_bar = Frame(root, bg=INPUT_BG, height=60)
input_bar.pack(fill="x")

user_entry = tk.Entry(
    input_bar,
    font=("Segoe UI", 11),
    bg="#020617",
    fg="white",
    insertbackground="white",
    relief="flat"
)
user_entry.pack(side="left", fill="x", expand=True, padx=15, pady=14)
user_entry.bind("<Return>", send_message)

send_btn = tk.Button(
    input_bar,
    text="➤",
    font=("Segoe UI", 14, "bold"),
    bg=USER_BUBBLE,
    fg="white",
    relief="flat",
    width=4,
    command=send_message
)
send_btn.pack(side="right", padx=15)

root.mainloop()
