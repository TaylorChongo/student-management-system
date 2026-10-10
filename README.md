# Student Course Management System

This is a console application built for the Python Basics lab. It demonstrates
lists, dictionaries, sets, comprehensions, reusable functions, abstract base
classes, encapsulation, inheritance, polymorphism, and magic methods.

## Requirements

- Python **3.14.8**
- No third-party runtime dependencies

## Setup

Create and activate a virtual environment using Python 3.14.8:

```powershell
py -3.14 -m venv .venv
.venv\Scripts\Activate.ps1
```

The project metadata is in `pyproject.toml`, and the exact interpreter range
is `>=3.14.8,<3.15`.

## Run the application

```powershell
python main.py
```

The menu supports registering students, adding courses, enrolling students,
recording grades, and generating student or instructor reports.

Data is saved automatically to `student_data.json` after changes and restored
when the application starts. The file is ignored by Git because it contains
local application data.

Example workflow:

```text
1. Register student
2. Add course
3. Enroll student in course
4. Record grade
5. View student summary
6. View course roster and average
```

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Module structure

- `main.py` - menu-driven CLI
- `student.py` - student base class and undergraduate/graduate subclasses
- `course.py` - course roster and grade management
- `enrollment.py` - immutable enrollment value object
- `services.py` - reusable operations and report generators
- `tests/` - automated tests for models, services, and CLI behavior
