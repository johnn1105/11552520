"""
This project is motivated by a real-life situation experienced by myself. 
One day, I arrived at a private music teacher’s studio for a scheduled lesson. 
However, the teacher had forgotten about the lesson because there was no proper scheduling system in place. 
The teacher relied mainly on memory and informal communication to manage lesson appointments. 
As a result, the lesson could not take place as planned.

In many small-scale teaching businesses, administrative tasks such as scheduling lessons and managing payments are often handled manually. 
This approach may work when the number of students is small, but as the number of students increases, 
it becomes increasingly difficult to keep track of lesson schedules and financial records.
In addition to scheduling issues, financial management is another challenge. Many tutors record payments manually or rely on messaging apps to confirm payments. 
This approach is prone to errors and makes it difficult to maintain accurate income records.
"""

# main.py
# Entry point of the project.
# - Start with CLI login
# - Option to launch GUI

from cli import run_cli_app

def main():
    run_cli_app()

if __name__ == "__main__":
    main()
