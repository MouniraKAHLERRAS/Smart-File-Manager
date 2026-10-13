# Smart File Manager

A desktop application built with Python to organize files automatically by category.

## Features

- Automatic file organization by extension
- Modern graphical interface built with CustomTkinter
- Simulation mode to preview changes before moving files
- Duplicate filename handling
- Statistics for moved files, ignored items, and errors
- Error logging and reporting
- Unit tests with pytest

## Technologies

- Python
- CustomTkinter
- pathlib
- shutil
- logging
- pytest

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd Smart-File-Manager
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the application

```bash
python interface.py
```

To run the tests:

```bash
python -m pytest -v
```

## Safety

Use simulation mode first. Real organization moves files into category folders.

## Author

Developed as a Python portfolio project.