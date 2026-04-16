# =========================================================
# Factory helpers to bootstrap the application
# =========================================================
from __future__ import annotations  # Allow forward references in type hints 
from constants import DATA_PATH  # Default path for storing student data 
from invoice import InvoiceService  # Service responsible for invoice generation logic
from repository import JsonStudentRepository  # Data access layer
from services import StudentService  # Core logic layer

def create_student_service(data_path: str = DATA_PATH) -> StudentService:
    #Create the fully wired student service."""
    
    # Step 1: Create repository (Data Layer)
    # This handles all persistence (loading/saving students from JSON file)
    repo = JsonStudentRepository(data_path)
    
    # Step 2: Create service (Business Logic Layer)
    # Inject repository into service (Dependency Injection)
    student_service = StudentService(repo)
    
    # Step 3: Create and attach invoice service
    # InvoiceService needs access to student data, so we pass student_service into it
    # Then we attach it back to student_service 
    student_service.attach_invoice_service(
        InvoiceService(student_service)
    )
    
    # Step 4: Return fully configured service
    return student_service