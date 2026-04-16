Music Lesson Management System

video present:
https://drive.google.com/file/d/1hyFMvWIx9Y9_DIFMDKBl-r0T-_gL_HwM/view?usp=drive_link

Overview
This project is a Music Lesson Management System developed in Python. It is designed for private music teachers to manage student records, lesson schedules, lesson changes, and financial operations such as invoice generation and monthly income reporting.

The system is inspired by real-life situations where lesson scheduling is handled manually using memory or informal communication, which may lead to missed lessons, duplicated bookings, and poor financial tracking.

Features

Student Management
The system allows users to add, edit, delete, and search for student records. Each student contains information such as name, instrument, grade, lesson time, fee, and lesson mode.

Lesson Scheduling
The system supports two types of scheduling:
Regular mode uses a fixed weekly schedule.
Flexible mode allows custom lesson dates for each student.

Lesson Change and Cancellation
Users can modify or cancel individual lessons. The system tracks these changes and reflects them in the schedule.

Conflict Detection
The system automatically checks for time conflicts between lessons and prevents overlapping schedules.

Invoice Generation
The system generates PDF invoices for each student based on the lessons in a given month.

Monthly Income Statement
The system can produce a monthly income report summarizing total earnings.

Dual Interface
The system supports both a Command Line Interface (CLI) and a Graphical User Interface (GUI) using Tkinter.

Validation System
All input data is validated through a centralized validation module to ensure data consistency and prevent errors.

System Flow

The system starts from main.py.
The user logs in through the CLI using a default account and password.
After login, the user can choose to continue using the CLI or open the GUI.

In CLI mode, the user interacts through menu options.
In GUI mode, the user interacts through a table-based interface and dialog forms.

All operations are processed through the service layer, which coordinates scheduling logic, validation, and data storage.

System Architecture

The system follows a layered architecture design:

Presentation Layer
CLI and GUI handle user interaction only.

Application Layer
StudentService acts as the main controller and coordinates all operations.

Business Logic Layer
ScheduleService handles scheduling and conflict detection.
InvoiceService handles invoice generation and financial reporting.

Data Layer
Repository manages data storage and retrieval using JSON.

Core Modules

main.py
Entry point of the application.

cli.py
Implements the command-line interface and login system.

gui.py
Implements the main graphical user interface.

gui_forms.py
Handles dialog windows for user input.

services.py
Coordinates student operations and acts as a facade layer.

schedule_service.py
Handles lesson scheduling, lesson changes, and conflict detection.

invoice.py
Handles invoice creation and PDF export.

lesson_plans.py
Implements different scheduling strategies for regular and flexible students.

repository.py
Manages data storage using JSON.

models.py
Defines core data structures such as Student, LessonOccurrence, and Invoice.

validators.py
Provides centralized validation logic for all inputs.

constants.py
Stores global configuration values.

Installation

Step 1: Download or clone the project files.

Step 2: Install required library
This project uses both built-in Python libraries and one external library.

Built-in Libraries (no installation required)

json (data storage handling)
datetime (date and time processing)
pathlib (file path management)
tkinter (GUI interface)

External Library 
reportlab (for generating PDF invoices and income reports)

Installation Command
pip install reportlab

Step 3: Run the program
python main.py

Login
Default account: 8090
Default password: 8090

CLI Mode
Users can manage students, schedules, and invoices through menu options.

GUI Mode
Users can interact with the system using a visual interface, including tables, buttons, and dialog forms.

Data Storage

All data is stored in a JSON file located at:
data/students.json

The file is automatically created if it does not exist.

Technical Highlights

The project demonstrates the use of Object-Oriented Programming concepts such as encapsulation, inheritance, abstraction, and polymorphism.

It also applies software design patterns including Strategy Pattern, Repository Pattern, and Facade Pattern.

The system includes real-world scheduling logic, validation mechanisms, and modular architecture design.

Limitations and Future Improvements

The system currently uses JSON for storage, which may not be efficient for large-scale data or concurrent access.

Future improvements may include database integration, user authentication, notification systems, and a web-based interface.
