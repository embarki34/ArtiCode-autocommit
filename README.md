
# ArtiCode-autocommit

🧠 **ArtiCode-autocommit** is a Python-based automation tool that auto-commits and pushes code changes to your Git repositories at scheduled times. Designed to simplify daily backups and ensure your work is always safely pushed to the `dev` branch.

---

## 📦 What This Tool Does

- Scans all Git repositories inside a given base directory.
- Checks for uncommitted changes.
- Commits the top modified files with a summary message.
- Pushes to the `dev` branch if you're on it.
- Logs all operations for traceability.
- Runs quietly in the system tray with a minimal UI.

---

## 📁 Directory Structure

```bash
ArtiCode-autocommit/
├── auto_committer.py      # Main script
├── auto_git_push.log      # Log file (auto-generated)
└── README.md              # This file
```

---

## ⚙️ Requirements

You need to have:

- Python 3.8+
- Git installed and available in your system PATH
- Pip packages:
  ```bash
  pip install schedule pystray pillow
  ```

---

## 🔧 Configuration

- **Edit the `REPO_BASE_DIR`** in the script to point to your project folder:
  ```python
  REPO_BASE_DIR = Path(r"C:\Users\<your-name>\Documents\projects")
  ```
- Ensure your repositories are using `dev` as the active working branch.

---

## 🧠 How It Works

1. **Startup**: When the script starts, it launches a tray icon in your system tray and begins a background scheduler.
2. **Scheduling**: By default, it runs at:
   - 🕚 11:00 AM
   - 🕓 4:20 PM
3. **Repository Scan**: It recursively looks for `.git` folders under `REPO_BASE_DIR`.
4. **Auto Commit**: If changes are found and you're on `dev`, it commits with a summary message.
5. **Push**: The commit is pushed to `origin/dev`.

---

## 🖥️ Running the App

Run the script:

```bash
python auto_committer.py
```

- It will add a system tray icon.
- The application will stay in the tray, silently pushing changes at scheduled times.
- You can exit it by right-clicking the tray icon and choosing "Quit".

---

## 📝 Example Log Output

```
[2025-06-04 11:00:01] 🔁 Git Auto Push Job started
[2025-06-04 11:00:02] ✅ Pushed <project-folder-name>: Auto backup: App.js (45 changes), index.css (22 changes)
[2025-06-04 11:00:02] ✅ Job finished.
```

---

## 🛠️ Creating an Executable

You can convert this script into a `.exe` file using **PyInstaller**:

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Navigate to your script folder

```bash
cd "C:\Users\<your-pc-name>\Documents\projects\ArtiCode-autocommit"
```

### 3. Build the Executable

```bash
pyinstaller --onefile --windowed auto_committer.py
```

- `--onefile`: Packages everything into a single `.exe`
- `--windowed`: Hides the console window (useful for tray apps)

If you want to **see console logs**, remove `--windowed`.

### 4. Output

The `.exe` will appear in the `dist` folder.

### 💡 Optional: Add an Icon

Put an `.ico` file in the folder and run:

```bash
pyinstaller --onefile --windowed --icon=icon.ico auto_committer.py
```

---

## 📌 Where to Use

Ideal for:

- Personal projects you work on frequently
- Ensuring daily backups without remembering to `git push`
- Developers who want version control hygiene with minimal effort

---

## 🤖 Credits

Made with ❤️ by Omar Embarki — for a clean and auto-backed-up workflow.
