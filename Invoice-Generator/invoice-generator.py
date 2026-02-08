import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("Smart Invoice Generator")
root.geometry("1100x700")
root.config(bg="#f2f4f7")

style = ttk.Style()
style.theme_use("clam")

# ================= VARIABLES =================
invoice_no = tk.StringVar(value=f"INV-{datetime.now().year}-001")
invoice_date = tk.StringVar(value=datetime.now().strftime("%d-%m-%Y"))
due_date = tk.StringVar(value=(datetime.now() + timedelta(days=7)).strftime("%d-%m-%Y"))

company_name = tk.StringVar(value="Your Company Name")
company_address = tk.StringVar(value="Company Address")
company_gst = tk.StringVar(value="GSTIN")

customer_name = tk.StringVar()
customer_phone = tk.StringVar()

item_name = tk.StringVar()
item_qty = tk.IntVar(value=1)
item_price = tk.DoubleVar(value=0.0)

subtotal = tk.DoubleVar(value=0.0)
tax = tk.DoubleVar(value=0.0)
total = tk.DoubleVar(value=0.0)

# ================= FUNCTIONS =================
def calculate_total():
    sub = 0
    for i in tree.get_children():
        sub += float(tree.item(i)["values"][3])
    subtotal.set(sub)
    tax.set(sub * 0.18)
    total.set(sub + tax)

def add_item():
    if not item_name.get() or item_qty.get() <= 0 or item_price.get() <= 0:
        messagebox.showerror("Error", "Enter valid item details")
        return

    amount = item_qty.get() * item_price.get()
    tree.insert("", "end",
                values=(item_name.get(), item_qty.get(), item_price.get(), amount))

    calculate_total()
    item_name.set("")
    item_qty.set(1)
    item_price.set(0.0)

def remove_item():
    selected = tree.selection()
    if selected:
        tree.delete(selected)
        calculate_total()

# ================= FIXED PDF FUNCTION =================
def export_pdf():
    try:
        if not tree.get_children():
            messagebox.showerror("Error", "Add at least one item before exporting PDF")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Invoice PDF",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile=f"{invoice_no.get()}.pdf"
        )

        if not file_path:
            return

        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        # ---------- HEADER ----------
        c.setFont("Helvetica-Bold", 16)
        c.drawString(40, height - 40, company_name.get())

        c.setFont("Helvetica", 10)
        c.drawString(40, height - 60, company_address.get())
        c.drawString(40, height - 75, f"GSTIN: {company_gst.get()}")

        c.drawRightString(width - 40, height - 40, f"Invoice: {invoice_no.get()}")
        c.drawRightString(width - 40, height - 60, f"Date: {invoice_date.get()}")
        c.drawRightString(width - 40, height - 75, f"Due: {due_date.get()}")

        # ---------- CUSTOMER ----------
        c.setFont("Helvetica-Bold", 11)
        c.drawString(40, height - 120, "Bill To:")

        c.setFont("Helvetica", 10)
        c.drawString(40, height - 140, customer_name.get())
        c.drawString(40, height - 155, customer_phone.get())

        # ---------- TABLE HEADER ----------
        y = height - 200
        c.setFont("Helvetica-Bold", 10)
        c.drawString(40, y, "Item")
        c.drawString(280, y, "Qty")
        c.drawString(340, y, "Price")
        c.drawString(430, y, "Amount")
        c.line(40, y - 5, width - 40, y - 5)

        # ---------- ITEMS ----------
        c.setFont("Helvetica", 10)
        y -= 25
        for row in tree.get_children():
            name, qty, price, amt = tree.item(row)["values"]
            c.drawString(40, y, str(name))
            c.drawString(280, y, str(qty))
            c.drawString(340, y, f"{price:.2f}")
            c.drawString(430, y, f"{amt:.2f}")
            y -= 20

        # ---------- TOTALS ----------
        y -= 20
        c.line(300, y, width - 40, y)

        c.drawRightString(500, y - 20, "Subtotal:")
        c.drawRightString(width - 40, y - 20, f"{subtotal.get():.2f}")

        c.drawRightString(500, y - 40, "Tax (18%):")
        c.drawRightString(width - 40, y - 40, f"{tax.get():.2f}")

        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(500, y - 65, "Total:")
        c.drawRightString(width - 40, y - 65, f"{total.get():.2f}")

        c.save()
        messagebox.showinfo("Success", f"Invoice PDF saved successfully:\n{file_path}")

    except Exception as e:
        messagebox.showerror("PDF Error", str(e))

# ================= UI =================
tk.Label(root, text="Smart Invoice Generator",
         bg="#2c3e50", fg="white",
         font=("Segoe UI", 20, "bold"),
         pady=15).pack(fill="x")

container = tk.Frame(root, bg="#f2f4f7")
container.pack(fill="both", expand=True, padx=20, pady=10)

# -------- Company & Invoice --------
info = tk.LabelFrame(container, text="Company & Invoice Details",
                     bg="white", padx=10, pady=10)
info.pack(fill="x")

fields = [
    ("Company Name", company_name),
    ("Address", company_address),
    ("GSTIN", company_gst),
    ("Invoice No", invoice_no),
    ("Invoice Date", invoice_date),
    ("Due Date", due_date)
]

for i, (lbl, var) in enumerate(fields):
    tk.Label(info, text=lbl, bg="white").grid(row=i // 3, column=(i % 3) * 2, padx=10, pady=5, sticky="w")
    tk.Entry(info, textvariable=var, width=30).grid(row=i // 3, column=(i % 3) * 2 + 1, padx=10)

# -------- Customer --------
cust = tk.LabelFrame(container, text="Customer Details",
                     bg="white", padx=10, pady=10)
cust.pack(fill="x", pady=10)

tk.Label(cust, text="Customer Name", bg="white").grid(row=0, column=0, padx=10)
tk.Entry(cust, textvariable=customer_name, width=30).grid(row=0, column=1)

tk.Label(cust, text="Phone", bg="white").grid(row=0, column=2, padx=10)
tk.Entry(cust, textvariable=customer_phone, width=20).grid(row=0, column=3)

# -------- Items --------
items = tk.LabelFrame(container, text="Items",
                      bg="white", padx=10, pady=10)
items.pack(fill="both", expand=True)

tk.Label(items, text="Item Name", bg="white").grid(row=0, column=0)
tk.Label(items, text="Qty", bg="white").grid(row=0, column=1)
tk.Label(items, text="Price", bg="white").grid(row=0, column=2)

tk.Entry(items, textvariable=item_name, width=30).grid(row=1, column=0, padx=5)
tk.Entry(items, textvariable=item_qty, width=10).grid(row=1, column=1)
tk.Entry(items, textvariable=item_price, width=15).grid(row=1, column=2)

tk.Button(items, text="Add Item", command=add_item).grid(row=1, column=3, padx=10)
tk.Button(items, text="Remove", command=remove_item).grid(row=1, column=4)

tree = ttk.Treeview(items,
                    columns=("Item", "Qty", "Price", "Amount"),
                    show="headings", height=8)

for col in ("Item", "Qty", "Price", "Amount"):
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.grid(row=2, column=0, columnspan=5, pady=10, sticky="nsew")

# -------- Summary --------
summary = tk.Frame(container, bg="white")
summary.pack(fill="x")

tk.Label(summary, text="Subtotal", bg="white").grid(row=0, column=0, padx=10)
tk.Entry(summary, textvariable=subtotal, state="readonly").grid(row=0, column=1)

tk.Label(summary, text="Tax (18%)", bg="white").grid(row=0, column=2)
tk.Entry(summary, textvariable=tax, state="readonly").grid(row=0, column=3)

tk.Label(summary, text="Total", bg="white",
         font=("Segoe UI", 10, "bold")).grid(row=0, column=4)
tk.Entry(summary, textvariable=total,
         font=("Segoe UI", 10, "bold"),
         state="readonly").grid(row=0, column=5)

# -------- Actions --------
actions = tk.Frame(root, bg="#f2f4f7")
actions.pack(fill="x", pady=10)

tk.Button(actions, text="Export Invoice PDF",
          width=20, bg="#27ae60", fg="white",
          font=("Segoe UI", 10, "bold"),
          command=export_pdf).pack(side="right", padx=20)

root.mainloop()
