# gui.py
# Tkinter GUI layer

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from services import StudentService
from invoice import generate_invoice_pdf
from models import Invoice

class App(tk.Tk):
    def __init__(self, service: StudentService):
        super().__init__()
        self.service = service
        self.title("Music Teacher Management System")
        self.geometry("980x520")

        # --- Left: student list ---
        left = ttk.Frame(self, padding=10)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(left, text="My Students").pack(anchor="w")
        self.tree = ttk.Treeview(left, columns=("id","name","instrument","weekday","fee","place"), show="headings", height=18)
        for col, label in [
            ("id","ID"),
            ("name","Name"),
            ("instrument","Instrument"),
            ("weekday","Lesson Day"),
            ("fee","Fee(HKD)"),
            ("place","Place"),
        ]:
            self.tree.heading(col, text=label)
            self.tree.column(col, width=130 if col!="name" else 200)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=8)

        btns = ttk.Frame(left)
        btns.pack(fill=tk.X)
        ttk.Button(btns, text="Refresh", command=self.refresh).pack(side=tk.LEFT, padx=4)
        ttk.Button(btns, text="Add", command=self.add_student).pack(side=tk.LEFT, padx=4)
        ttk.Button(btns, text="Edit", command=self.edit_student).pack(side=tk.LEFT, padx=4)
        ttk.Button(btns, text="Delete", command=self.delete_student).pack(side=tk.LEFT, padx=4)

        # --- Right: schedule + invoice ---
        right = ttk.Frame(self, padding=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(right, text="Schedule (One Month)").pack(anchor="w")
        top = ttk.Frame(right)
        top.pack(fill=tk.X, pady=6)
        ttk.Label(top, text="Month (YYYY-MM):").pack(side=tk.LEFT)
        self.month_var = tk.StringVar(value="2026-02")
        ttk.Entry(top, textvariable=self.month_var, width=10).pack(side=tk.LEFT, padx=6)
        ttk.Button(top, text="Show Schedule", command=self.show_schedule).pack(side=tk.LEFT, padx=6)

        self.schedule_box = tk.Text(right, height=16, width=45)
        self.schedule_box.pack(fill=tk.BOTH, expand=True, pady=6)

        inv = ttk.Frame(right)
        inv.pack(fill=tk.X)
        ttk.Button(inv, text="Generate Invoice (Selected Student)", command=self.generate_invoice).pack(side=tk.LEFT)

        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for s in self.service.list_students():
            self.tree.insert("", tk.END, values=(s.student_id, s.name, s.instrument, s.lesson_weekday, s.fee_hkd, s.place))

    def _selected_student_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        values = self.tree.item(sel[0], "values")
        return int(values[0])

    def add_student(self):
        try:
            name = simpledialog.askstring("Add Student", "Name:")
            if not name:
                return
            birth = simpledialog.askstring("Add Student", "Birth (yyyy-mm-dd):", initialvalue="2001-01-01")
            instr = simpledialog.askstring("Add Student", "Instrument:", initialvalue="Trumpet")
            grade = simpledialog.askinteger("Add Student", "Grade:", initialvalue=8)
            mins = simpledialog.askinteger("Add Student", "Lesson minutes:", initialvalue=45)
            fee = simpledialog.askinteger("Add Student", "Fee (HKD):", initialvalue=500)
            weekday = simpledialog.askstring("Add Student", "Lesson weekday (Mon..Sun):", initialvalue="Mon")
            place = simpledialog.askstring("Add Student", "Place (Studio/Home):", initialvalue="Studio")

            self.service.add_student(name, birth, instr, grade, mins, fee, weekday, place)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def edit_student(self):
        sid = self._selected_student_id()
        if sid is None:
            messagebox.showinfo("Info", "Please select a student first.")
            return

        s = self.service.repo.get_by_id(sid)
        if not s:
            messagebox.showerror("Error", "Student not found.")
            return

        try:
            name = simpledialog.askstring("Edit Student", "Name:", initialvalue=s.name) or s.name
            birth = simpledialog.askstring("Edit Student", "Birth (yyyy-mm-dd):", initialvalue=s.birth_date.isoformat()) or s.birth_date.isoformat()
            instr = simpledialog.askstring("Edit Student", "Instrument:", initialvalue=s.instrument) or s.instrument
            grade = simpledialog.askinteger("Edit Student", "Grade:", initialvalue=s.grade) or s.grade
            mins = simpledialog.askinteger("Edit Student", "Lesson minutes:", initialvalue=s.lesson_minutes) or s.lesson_minutes
            fee = simpledialog.askinteger("Edit Student", "Fee (HKD):", initialvalue=s.fee_hkd) or s.fee_hkd
            weekday = simpledialog.askstring("Edit Student", "Lesson weekday (Mon..Sun):", initialvalue=s.lesson_weekday) or s.lesson_weekday
            place = simpledialog.askstring("Edit Student", "Place (Studio/Home):", initialvalue=s.place) or s.place

            y, m, d = map(int, birth.split("-"))
            import datetime
            s.name = name
            s.birth_date = datetime.date(y, m, d)
            s.instrument = instr
            s.grade = int(grade)
            s.lesson_minutes = int(mins)
            s.fee_hkd = int(fee)
            s.lesson_weekday = weekday
            s.place = place

            self.service.update_student(s)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_student(self):
        sid = self._selected_student_id()
        if sid is None:
            messagebox.showinfo("Info", "Please select a student first.")
            return
        if messagebox.askyesno("Confirm", f"Delete student ID={sid}?"):
            self.service.delete_student_by_id(sid)
            self.refresh()

    def show_schedule(self):
        self.schedule_box.delete("1.0", tk.END)
        ym = self.month_var.get().strip() or "2026-02"
        try:
            year, month = map(int, ym.split("-"))
            items = self.service.schedule_for_month(year, month)
            if not items:
                self.schedule_box.insert(tk.END, "(No schedule)\n")
                return
            for name, dt in items:
                self.schedule_box.insert(tk.END, f"{dt} - {name}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generate_invoice(self):
        sid = self._selected_student_id()
        if sid is None:
            messagebox.showinfo("Info", "Please select a student first.")
            return

        ym = self.month_var.get().strip() or "2026-02"
        try:
            year, month = map(int, ym.split("-"))
            s = self.service.repo.get_by_id(sid)
            if not s:
                messagebox.showerror("Error", "Student not found.")
                return

            dates = self.service.lesson_dates_in_month(year, month, s.lesson_weekday)
            total = s.fee_hkd * len(dates)
            invoice_no = f"{year}{month:02d}-{sid}-0001"

            inv = Invoice(
                invoice_no=invoice_no,
                month=ym,
                student_name=s.name,
                instrument=s.instrument,
                grade=s.grade,
                lesson_dates=dates,
                fee_hkd=s.fee_hkd,
                total_hkd=total
            )
            path = generate_invoice_pdf(inv)
            messagebox.showinfo("Done", f"Invoice generated:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def run_gui_app(service: StudentService):
    app = App(service)
    app.mainloop()
