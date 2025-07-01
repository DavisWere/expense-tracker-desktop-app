# 💸 Finance Tracker Desktop App

A personal finance tracker to manage income, expenses, budgets, and generate PDF/email reports.

Built using **Python + Tkinter + SQLite**, with offline support and Gmail integration for report delivery.

---

## 📦 1. Installation

### ✅ Requirements:

- Python 3.10 or newer
- pip (Python package manager)

### 🖥️ Supported OS:

- Windows
- Linux (e.g., Ubuntu)
- macOS (minor path tweaks may be needed)

### 🔧 Setup

Clone the repo:

```bash
git  clone https://github.com/DavisWere/expense-tracker-desktop-app.git
cd expense-tracker-desktop-app
```

Create and activate a virtual environment:

```bash
python3 -m venv env
source env/bin/activate   # Linux/macOS
# OR
env\Scripts\activate      # Windows
```

Install required libraries:

```bash
pip install -r requirements.txt
```

---

## 🚀 2. Running the App

### 👇 Start the app:

```bash
python main.py
```

### Features:

- Register and Login using email
- Add/view transactions
- Filter by category/date
- Export PDF reports
- Email reports (background task)
- Persistent login saved in `current_user.json`

---

## 🛠️ 3. Convert to Standalone App (No Python Needed)

### 📁 One-folder distribution (recommended)

Use **PyInstaller** to bundle the app:

```bash
pip install pyinstaller
```

Then run:

```bash
pyinstaller main.py --add-data "credentials.json:." --noconfirm --windowed
```

### 📁 After build:

Find your app in:

```
dist/
└── main/
    ├── main.exe (Windows) or `main` (Linux)
    ├── credentials.json
    ├── token.pickle (after first Gmail auth)
    ├── finance.db (auto-created)
    └── current_user.json (auto-created)
```

Zip the `dist/main/` folder and share it!

To run the app:

```bash
cd dist/main
./main       # or main.exe on Windows
```

---

## 📧 Gmail Setup for Email Reports

1. Place your `credentials.json` in the project folder.
2. First run will open a browser window to authenticate your Gmail.
3. It creates `token.pickle` for future logins.

✅ Email reports are auto-sent monthly (or test every 2 min in dev).

---

## 🔒 Sensitive Files

Add these to `.gitignore`:

```
credentials.json
token.pickle
current_user.json
finance.db
*.pdf
```

---

## Developer Notes

- All session and user data are saved locally.
- PDF reports are named like: `report_2025-07-01.pdf`
- To test email without waiting:
  - Edit background schedule to `schedule.every(2).minutes.do(...)`

---

## ✅ Quick Commands

```bash
# Run the app
python main.py

# Build standalone
pyinstaller main.py --add-data "credentials.json:." --noconfirm --windowed

# Clean build
rm -rf build dist __pycache__ main.spec
```

---

📌 **Support:** If any feature fails (like email), check `error.log` for details. If you need help, feel free to ask. 😊

```bash
devisodhis10@gmail.com
vicmwe184@gmail.com
```

Enjoy tracking your finances! 💼
Free to use and modify (No copyright intended)
