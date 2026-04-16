# =========================================================
# Shared constants for the application.
# This file defines all global constants used across the application.
# It centralizes configuration values, allowed input options, and
# default data to ensure consistency
# =========================================================
from __future__ import annotations
# File path for persistent student storage (JSON)
DATA_PATH = "data/students.json"

# Default account 
DEFAULT_ACCOUNT = "8090"
DEFAULT_PASSWORD = "8090"

# Default month
DEFAULT_MONTH_TEXT = "2026-02"
DEFAULT_OUTPUT_DIR = "output"

# Allowed values for various student attributes
ALLOWED_GRADES = ["1", "2", "3", "4", "5", "6", "7", "8", "ATCL", "LTCL", "FTCL"]
ALLOWED_LESSON_MINUTES = [30, 45, 60, 90]
ALLOWED_WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
ALLOWED_PLACES = ["Studio", "Home"]
PLAN_TYPES = ["regular", "flexible"]

# Mapping of weekday names to indices (0=Mon, 6=Sun) for easier processing
WEEKDAY_MAP = {weekday_name: index for index, weekday_name in enumerate(ALLOWED_WEEKDAYS)}
WEEKDAY_NAME_BY_INDEX = {index: weekday_name for weekday_name, index in WEEKDAY_MAP.items()}

# Default students
DEFAULT_STUDENTS = [
    ("John Chan", "2001-01-01", "Trumpet", "8", 45, "0900", 500, "Mon", "Studio"),
    ("Alan Lee", "2002-03-12", "Piano", "6", 45, "1000", 450, "Tue", "Studio"),
    ("Jace Wong", "2003-07-20", "Violin", "5", 45, "1100", 400, "Wed", "Home"),
    ("Mary Ho", "2000-11-02", "Flute", "7", 45, "1200", 480, "Thu", "Studio"),
    ("Chris Lau", "2004-09-14", "Drums", "4", 60, "1330", 550, "Fri", "Home"),
    ("Emily Ng", "2005-05-10", "Guitar", "6", 45, "1500", 420, "Sat", "Studio"),
    ("David Chan", "2002-12-25", "Saxophone", "7", 45, "1600", 500, "Sun", "Home"),
    ("Sophia Lam", "2003-08-18", "Cello", "5", 60, "1700", 530, "Mon", "Studio"),
    ("Daniel Cheung", "2001-04-30", "Clarinet", "6", 45, "1830", 460, "Tue", "Home"),
    ("Kevin Yeung", "2004-06-22", "Trombone", "5", 45, "2000", 470, "Wed", "Studio"),
]
