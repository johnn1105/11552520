# cli.py
# 1. Handle user login
# 2. Provide a CLI menu
# 3. service-layer functions 
# 4. launch the GUI

from datetime import datetime
from repository import JsonStudentRepository
from services import StudentService
# Path to the JSON file used to store student data
DATA_PATH = "data/students.json"
# Default login credentials
DEFAULT_ACC = "8090"
DEFAULT_PW = "8090"

def login_cli() -> bool:
    print("=== Login System (CLI) ===")
    acc = input(f"Account (default {DEFAULT_ACC}): ").strip() or DEFAULT_ACC
    pw = input(f"Password (default {DEFAULT_PW}): ").strip() or DEFAULT_PW
    # Validate login credentials
    if acc == DEFAULT_ACC and pw == DEFAULT_PW:
        print("Login success.\n")
        return True
    print("Login failed.\n")
    return False

def print_students(service: StudentService) -> None:
    students = service.list_students()
    if not students:
        print("(No students)")
        return
    print("=== My Students ===")
    for s in students:
        print(
            f"ID={s.student_id} | Name={s.name} | Birth={s.birth_date} | "
            f"Instrument={s.instrument} | Grade={s.grade} | Time={s.lesson_minutes}min | "
            f"Fee=HKD{s.fee_hkd} | Lesson={s.lesson_weekday} | Place={s.place}"
        )

def add_student_cli(service: StudentService) -> None:
    print("=== Add Student ===")
    name = input("Name: ").strip()
    birth = input("Birth (yyyy-mm-dd): ").strip()
    instr = input("Instrument: ").strip()
    grade = int(input("Grade (e.g. 8): ").strip())
    mins = int(input("Lesson time minutes (e.g. 45): ").strip())
    fee = int(input("Fee HKD (e.g. 500): ").strip())
    weekday = input("Lesson per week (Mon/Tue/...): ").strip()
    place = input("Place (Studio/Home): ").strip()

    s = service.add_student(name, birth, instr, grade, mins, fee, weekday, place)
    print(f"Added: {s.display_name()}")

def edit_student_cli(service: StudentService) -> None:
    print("=== Edit Student ===")
    sid = int(input("Student ID: ").strip())
    s = service.repo.get_by_id(sid)
    if not s:
        print("Student not found.")
        return

    name = input(f"Name ({s.name}): ").strip() or s.name
    birth = input(f"Birth ({s.birth_date}): ").strip() or s.birth_date.isoformat()
    instr = input(f"Instrument ({s.instrument}): ").strip() or s.instrument
    grade = input(f"Grade ({s.grade}): ").strip() or str(s.grade)
    mins = input(f"Time minutes ({s.lesson_minutes}): ").strip() or str(s.lesson_minutes)
    fee = input(f"Fee HKD ({s.fee_hkd}): ").strip() or str(s.fee_hkd)
    weekday = input(f"Lesson weekday ({s.lesson_weekday}): ").strip() or s.lesson_weekday
    place = input(f"Place ({s.place}): ").strip() or s.place

    y, m, d = map(int, birth.split("-"))
    s.name = name
    s.birth_date = __import__("datetime").date(y, m, d)
    s.instrument = instr
    s.grade = int(grade)
    s.lesson_minutes = int(mins)
    s.fee_hkd = int(fee)
    s.lesson_weekday = weekday
    s.place = place

    service.update_student(s)
    print("Updated.")

def delete_student_cli(service: StudentService) -> None:
    print("=== Delete Student ===")
    mode = input("Delete by (1) ID or (2) Name? ").strip()
    if mode == "1":
        sid = int(input("Student ID: ").strip())
        service.delete_student_by_id(sid)
        print("Deleted (if existed).")
    elif mode == "2":
        keyword = input("Name keyword: ").strip()
        matches = service.find_by_name(keyword)
        if not matches:
            print("No match.")
            return
        print("Matched students:")
        for s in matches:
            print(f"- {s.display_name()}")
        sid = int(input("Enter the ID to delete: ").strip())
        service.delete_student_by_id(sid)
        print("Deleted (if existed).")
    else:
        print("Invalid choice.")

def show_schedule_cli(service: StudentService) -> None:
    print("=== Show Schedule (One Month) ===")
    ym = input("Enter month (YYYY-MM), default 2026-02: ").strip() or "2026-02"
    year, month = map(int, ym.split("-"))
    schedule = service.schedule_for_month(year, month)

    if not schedule:
        print("(No schedule)")
        return

    for name, dt in schedule:
        print(f"{dt} - {name}")

def invoice_cli(service: StudentService) -> None:
    pass

def run_cli_menu(service: StudentService) -> None:
    while True:
        print("\n=== Music Teacher Management ===")
        print("1) View my students")
        print("2) Add student")
        print("3) Edit student")
        print("4) Delete student")
        print("5) Show my schedule in one month")
        print("6) Generate invoice")
        print("0) Exit")
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                print_students(service)
            elif choice == "2":
                add_student_cli(service)
            elif choice == "3":
                edit_student_cli(service)
            elif choice == "4":
                delete_student_cli(service)
            elif choice == "5":
                show_schedule_cli(service)
            elif choice == "6":
                invoice_cli(service)
            elif choice == "0":
                print("Bye.")
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"[Error] {e}")

def run_cli_app() -> None:
    if not login_cli():
        return

    repo = JsonStudentRepository(DATA_PATH)
    service = StudentService(repo)
    service.ensure_default_student() 

    ans = input("Enter to system (GUI)? (y/n): ").strip().lower()
    if ans == "y":
        from gui import run_gui_app
        run_gui_app(service)
    else:
        run_cli_menu(service)
