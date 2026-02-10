import customtkinter as ctk
import sqlite3
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog, messagebox
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- UI CONFIG ---------------- #
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- DATABASE ---------------- #
conn = sqlite3.connect("study_pro_ui.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS study_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    duration INTEGER,
    mood TEXT,
    date TEXT
)
""")
conn.commit()

# ---------------- APP ---------------- #
class StudyProUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("AI Study Pattern Analyzer PRO")
        self.geometry("1250x720")
        self.minsize(1100, 650)

        self.build_sidebar()
        self.build_header()
        self.build_pages()
        self.show_page("dashboard")

    # ---------------- LAYOUT ---------------- #
    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            self.sidebar,
            text="Study Analyzer",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=25)

        self.nav_buttons = {}
        for page in ["dashboard", "log", "analytics", "ai", "reports"]:
            btn = ctk.CTkButton(
                self.sidebar,
                text=page.capitalize(),
                height=40,
                corner_radius=8,
                command=lambda p=page: self.show_page(p)
            )
            btn.pack(fill="x", padx=20, pady=6)
            self.nav_buttons[page] = btn

    def build_header(self):
        self.header = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.header.pack(side="top", fill="x")

        self.header_label = ctk.CTkLabel(
            self.header,
            text="Dashboard",
            font=("Segoe UI", 22, "bold")
        )
        self.header_label.pack(side="left", padx=25, pady=15)

    def build_pages(self):
        self.container = ctk.CTkFrame(self)
        self.container.pack(expand=True, fill="both", padx=20, pady=20)

        self.pages = {
            "dashboard": self.dashboard_page(),
            "log": self.log_page(),
            "analytics": self.analytics_page(),
            "ai": self.ai_page(),
            "reports": self.report_page()
        }

    def show_page(self, page):
        for p in self.pages.values():
            p.pack_forget()
        self.pages[page].pack(expand=True, fill="both")
        self.header_label.configure(text=page.capitalize())

    # ---------------- PAGES ---------------- #
    def dashboard_page(self):
        frame = ctk.CTkFrame(self.container)

        ctk.CTkLabel(
            frame,
            text="Welcome Back 👋",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            frame,
            text="Track • Analyze • Improve your study habits",
            font=("Segoe UI", 14),
            text_color="gray"
        ).pack()

        return frame

    def log_page(self):
        frame = ctk.CTkFrame(self.container)

        card = ctk.CTkFrame(frame, width=400)
        card.pack(pady=40)

        ctk.CTkLabel(card, text="Log Study Session", font=("Segoe UI", 18, "bold")).pack(pady=15)

        self.subject = ctk.CTkEntry(card, placeholder_text="Subject")
        self.subject.pack(padx=20, pady=10)

        self.duration = ctk.CTkEntry(card, placeholder_text="Duration (minutes)")
        self.duration.pack(padx=20, pady=10)

        self.mood = ctk.CTkOptionMenu(card, values=["Focused", "Normal", "Tired", "Stressed"])
        self.mood.pack(padx=20, pady=10)

        ctk.CTkButton(card, text="Save Session", command=self.save_session).pack(pady=20)

        return frame

    def analytics_page(self):
        frame = ctk.CTkFrame(self.container)

        ctk.CTkButton(frame, text="Subject Analytics", command=self.subject_chart).pack(pady=10)
        ctk.CTkButton(frame, text="Daily Trend", command=self.daily_chart).pack(pady=10)

        return frame

    def ai_page(self):
        frame = ctk.CTkFrame(self.container)

        self.ai_box = ctk.CTkTextbox(frame, font=("Segoe UI", 14))
        self.ai_box.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkButton(frame, text="Generate AI Coaching", command=self.ai_insights).pack(pady=10)

        return frame

    def report_page(self):
        frame = ctk.CTkFrame(self.container)

        ctk.CTkButton(frame, text="Export CSV", command=self.export_csv).pack(pady=10)
        ctk.CTkButton(frame, text="Export PDF", command=self.export_pdf).pack(pady=10)

        return frame

    # ---------------- LOGIC ---------------- #
    def save_session(self):
        cur.execute(
            "INSERT INTO study_logs VALUES (NULL, ?, ?, ?, ?)",
            (
                self.subject.get(),
                int(self.duration.get()),
                self.mood.get(),
                datetime.now().strftime("%Y-%m-%d")
            )
        )
        conn.commit()
        messagebox.showinfo("Saved", "Study session logged successfully")

    def get_df(self):
        return pd.read_sql("SELECT * FROM study_logs", conn)

    def subject_chart(self):
        df = self.get_df()
        df.groupby("subject")["duration"].sum().plot(kind="bar", title="Study by Subject")
        plt.show()

    def daily_chart(self):
        df = self.get_df()
        df.groupby("date")["duration"].sum().plot(marker="o", title="Daily Study Trend")
        plt.show()

    def ai_insights(self):
        df = self.get_df()
        self.ai_box.delete("1.0", "end")

        avg = df["duration"].mean()
        burnout = avg > 180

        text = f"""
📊 Study Analysis
• Average Session: {int(avg)} minutes

🧠 AI Coach:
• Best focus window: Morning
• Use 90-minute deep work blocks
• Avoid studying late night continuously

{"⚠ Burnout risk detected" if burnout else "✅ Healthy study routine"}
"""
        self.ai_box.insert("end", text)

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        self.get_df().to_csv(path, index=False)

    def export_pdf(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf")
        doc = SimpleDocTemplate(path)
        styles = getSampleStyleSheet()
        story = [Paragraph("Study Pattern Report", styles["Title"])]

        for _, row in self.get_df().iterrows():
            story.append(Paragraph(str(dict(row)), styles["Normal"]))

        doc.build(story)

# ---------------- RUN ---------------- #
if __name__ == "__main__":
    app = StudyProUI()
    app.mainloop()
