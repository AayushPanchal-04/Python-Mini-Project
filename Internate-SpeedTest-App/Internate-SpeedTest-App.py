import customtkinter as ctk
import speedtest
import threading

# ---------------- UI THEME ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SpeedTestApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Internet Speed Test – Office")
        self.geometry("1100x650")
        self.minsize(1100, 650)

        # ---------- HEADER ----------
        header = ctk.CTkFrame(self, height=80, corner_radius=0)
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text="Internet Speed Test",
            font=("Segoe UI", 28, "bold")
        ).pack(side="left", padx=30, pady=20)

        # ---------- MAIN ----------
        main = ctk.CTkFrame(self, corner_radius=15)
        main.pack(expand=True, fill="both", padx=30, pady=25)

        # LEFT PANEL
        left = ctk.CTkFrame(main, corner_radius=15)
        left.pack(side="left", expand=True, fill="both", padx=20, pady=20)

        self.big_speed = ctk.CTkLabel(
            left,
            text="-- Mbps",
            font=("Segoe UI", 52, "bold")
        )
        self.big_speed.pack(pady=30)

        self.speed_type = ctk.CTkLabel(
            left,
            text="Download Speed",
            font=("Segoe UI", 16)
        )
        self.speed_type.pack()

        self.status = ctk.CTkLabel(
            left,
            text="Click START to test internet speed",
            font=("Segoe UI", 14)
        )
        self.status.pack(pady=20)

        self.start_btn = ctk.CTkButton(
            left,
            text="START",
            width=220,
            height=55,
            font=("Segoe UI", 18, "bold"),
            command=self.start_test
        )
        self.start_btn.pack(pady=25)

        # RIGHT PANEL
        right = ctk.CTkFrame(main, corner_radius=15)
        right.pack(side="right", fill="y", padx=20, pady=20)

        self.dl = self.row(right, "Download", "-- Mbps")
        self.ul = self.row(right, "Upload", "-- Mbps")
        self.ping = self.row(right, "Ping", "-- ms")
        self.isp = self.row(right, "ISP", "--")
        self.server = self.row(right, "Server", "--")

        self.quality = ctk.CTkLabel(
            right,
            text="Connection Quality: --",
            font=("Segoe UI", 16, "bold")
        )
        self.quality.pack(pady=20)

        self.note = ctk.CTkLabel(
            self,
            text="Results are estimated and may vary depending on network conditions",
            font=("Segoe UI", 11)
        )
        self.note.pack(pady=10)

    def row(self, parent, label, value):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", pady=8, padx=15)

        ctk.CTkLabel(f, text=label, font=("Segoe UI", 14)).pack(side="left")
        v = ctk.CTkLabel(f, text=value, font=("Segoe UI", 14, "bold"))
        v.pack(side="right")
        return v

    # ---------------- SPEED TEST ----------------
    def start_test(self):
        self.start_btn.configure(state="disabled", text="Testing...")
        self.status.configure(text="Running speed test...")
        threading.Thread(target=self.run_test, daemon=True).start()

    def run_test(self):
        try:
            st = speedtest.Speedtest()
            st.get_best_server()

            downloads = []
            uploads = []

            for i in range(2):  # ⬅ run twice for stability
                downloads.append(st.download() / 1_000_000)
                uploads.append(st.upload() / 1_000_000)

            download = round(sum(downloads) / len(downloads), 2)
            upload = round(sum(uploads) / len(uploads), 2)
            ping = round(st.results.ping, 2)

            isp = st.results.client.get("isp", "Unknown")
            server = st.results.server.get("name", "Unknown")

            self.after(0, self.update_ui, download, upload, ping, isp, server)

        except Exception:
            self.after(0, self.status.configure,
                       {"text": "Error checking speed. Check internet."})
            self.after(0, self.start_btn.configure,
                       {"state": "normal", "text": "START"})

    def update_ui(self, d, u, p, isp, server):
        self.big_speed.configure(text=f"{d} Mbps")
        self.dl.configure(text=f"{d} Mbps")
        self.ul.configure(text=f"{u} Mbps")
        self.ping.configure(text=f"{p} ms")
        self.isp.configure(text=isp)
        self.server.configure(text=server)

        self.quality.configure(text=f"Connection Quality: {self.get_quality(d)}")

        self.status.configure(text="Speed test completed")
        self.start_btn.configure(state="normal", text="RETEST")

    def get_quality(self, speed):
        if speed < 5:
            return "Poor ❌"
        elif speed < 25:
            return "Average ⚠️"
        elif speed < 100:
            return "Good ✅"
        else:
            return "Excellent 🚀"

# ---------------- RUN ----------------
if __name__ == "__main__":
    app = SpeedTestApp()
    app.mainloop()
