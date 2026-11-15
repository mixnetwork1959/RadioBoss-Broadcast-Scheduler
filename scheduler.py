# ==========================================
# Broadcast Scheduler
# Version 4.5.0
# scheduler.py
# ==========================================

from config import load_settings
from config import save_settings
from database import Database
from scheduler_controller import SchedulerController
from gui import show_events
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

VERSION = "4.5.0"


def main():

    print("=" * 45)
    print(f" Broadcast Scheduler v{VERSION}")
    print("=" * 45)

    # Load settings
    settings = load_settings()

    # A fresh portable installation has no settings.json. Do not crash:
    # ask for the RadioBOSS schedule and save its path for later launches.
    if not Path(settings.get("admin_sdl", "")).is_file():
        dialog_root = tk.Tk()
        dialog_root.withdraw()
        try:
            messagebox.showinfo(
                "Broadcast Scheduler – First Setup",
                "Select your RadioBOSS scheduler (.sdl) file.",
                parent=dialog_root,
            )
            selected = filedialog.askopenfilename(
                parent=dialog_root,
                title="Select RadioBOSS SDL file",
                filetypes=[("RadioBOSS schedule", "*.sdl"), ("All files", "*.*")],
            )
            if not selected:
                print("No SDL file selected. Startup cancelled.")
                return
            settings["admin_sdl"] = selected
            save_settings(settings)
        finally:
            dialog_root.destroy()

    # Open database
    db = Database(settings)

    # Load events
    events = db.load_events()
    print(f"Events loaded: {len(events)}")

    # Create controller
    controller = SchedulerController(events)

    # Generate current week
    runtimes = controller.refresh()
    print(f"RunTimes generated: {len(runtimes)}")

    print("Schedule analysis completed.")

    # Start GUI
    show_events(
        controller,
        runtimes,
        settings
    )


if __name__ == "__main__":
    main()
