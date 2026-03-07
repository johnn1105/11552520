# gui.py
# Tkinter GUI layer

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


def run_gui_app(service: StudentService):
    app = App(service)
    app.mainloop()
