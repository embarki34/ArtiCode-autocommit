import os
import subprocess
from pathlib import Path
from datetime import datetime
import time
import threading
import schedule
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

REPO_BASE_DIR = Path(r"C:\Users\oembarki\OneDrive - condor.dz\Documents\projects")  # 🔁 Change to your actual projects directory

# === LOGGING ===
def ensure_log_directory():
    log_dir = Path(__file__).parent
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir

LOG_FILE = ensure_log_directory() / "auto_git_push.log"
print(f"Log file will be created at: {LOG_FILE.absolute()}")

def log(message):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_msg = f"[{timestamp}] {message}"
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(full_msg + "\n")
        print(full_msg)  # Also print to console for visibility
    except Exception as e:
        print(f"Error writing to log file: {e}")
        print(f"Attempted to write: {message}")

# === UTILITIES ===
def run_cmd(cmd, path):
    result = subprocess.run(cmd, cwd=path, capture_output=True, text=True, shell=True)
    return result.stdout.strip()

def is_on_dev_branch(repo_path):
    branch = run_cmd("git rev-parse --abbrev-ref HEAD", repo_path)
    return branch == "dev"

def get_changed_files(repo_path):
    return run_cmd("git status --porcelain", repo_path)

def get_top_changed_files(repo_path):
    output = run_cmd("git diff --numstat", repo_path)
    lines = output.splitlines()
    changes = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 3:
            added, deleted, filename = parts
            try:
                total = int(added) + int(deleted)
                changes.append((filename, total))
            except ValueError:
                continue
    changes.sort(key=lambda x: x[1], reverse=True)
    return changes[:3]

def auto_commit_and_push(repo_path):
    if not is_on_dev_branch(repo_path):
        log(f"⏩ Skipped {repo_path.name}: not on 'dev' branch.")
        return

    status = get_changed_files(repo_path)
    if not status:
        log(f"📁 No changes in {repo_path.name}.")
        return

    run_cmd("git add .", repo_path)
    top_files = get_top_changed_files(repo_path)
    summary = ", ".join(f"{f} ({c} changes)" for f, c in top_files)
    commit_msg = f"Auto backup: {summary or 'minor edits'}"
    run_cmd(f'git commit -m "{commit_msg}"', repo_path)
    run_cmd("git push origin dev", repo_path)
    log(f"✅ Pushed {repo_path.name}: {commit_msg}")

def find_git_repos(base_path):
    for root, dirs, files in os.walk(base_path):
        if ".git" in dirs:
            yield Path(root)

def job():
    log("🔁 Git Auto Push Job started")
    for repo in find_git_repos(REPO_BASE_DIR):
        try:
            auto_commit_and_push(repo)
        except Exception as e:
            log(f"❌ Error in {repo.name}: {e}")
    log("✅ Job finished.\n")

# === SYSTEM TRAY UI ===
def create_image():
    # Creates a small black icon (you can replace with real .ico if needed)
    image = Image.new("RGB", (64, 64), "black")
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 16, 48, 48), fill="green")
    return image

def setup_tray_icon():
    icon = Icon("AutoGit")

    def on_quit(icon, item):
        log("❎ Tray app exited by user.")
        icon.stop()

    icon.icon = create_image()
    icon.menu = Menu(MenuItem("Quit", on_quit))
    return icon

# === BACKGROUND SCHEDULER ===
def start_scheduler():
    schedule.every().day.at("11:00").do(job)
    schedule.every().day.at("16:20").do(job)

    while True:
        schedule.run_pending()
        time.sleep(30)

# === MAIN ===
if __name__ == "__main__":
    log("🟢 Tray app started")
    threading.Thread(target=start_scheduler, daemon=True).start()
    tray = setup_tray_icon()
    tray.run()
