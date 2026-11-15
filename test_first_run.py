"""Regression checks for portable SDL selection and schedule compatibility."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import config
import scheduler
from database import Database
from scheduler_controller import SchedulerController


class PortableFirstRunTests(unittest.TestCase):
    def test_runtime_hook_sets_only_existing_bundle_paths(self):
        import tk_runtime_hook

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "_tcl_data").mkdir()
            (root / "_tk_data").mkdir()
            (root / "_tcl_data" / "init.tcl").touch()
            (root / "_tk_data" / "tk.tcl").touch()
            with patch.object(tk_runtime_hook.sys, "_MEIPASS", directory, create=True), \
                 patch.dict(os.environ, {}, clear=True):
                tk_runtime_hook.configure_tk_paths()
                self.assertEqual(os.environ["TCL_LIBRARY"], str(root / "_tcl_data"))
                self.assertEqual(os.environ["TK_LIBRARY"], str(root / "_tk_data"))

    def test_missing_settings_gets_default_values(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(config, "SETTINGS_FILE", Path(directory) / "settings.json"):
                self.assertEqual(config.load_settings()["admin_sdl"], "")

    def test_first_run_prompts_and_saves_selected_sdl(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "settings.json"
            selected_sdl = Path(directory) / "RadioBoss.sdl"
            selected_sdl.write_text("[event0]\nTaskName=Test\n", encoding="utf-8")
            root = MagicMock()
            with patch.object(config, "SETTINGS_FILE", file_path), \
                 patch.object(scheduler, "load_settings", side_effect=config.load_settings), \
                 patch.object(scheduler, "save_settings", side_effect=config.save_settings), \
                 patch.object(scheduler.tk, "Tk", return_value=root), \
                 patch.object(scheduler.messagebox, "showinfo"), \
                 patch.object(scheduler.filedialog, "askopenfilename", return_value=str(selected_sdl)), \
                 patch.object(scheduler, "show_events"):
                scheduler.main()
            self.assertEqual(json.loads(file_path.read_text(encoding="utf-8"))["admin_sdl"], str(selected_sdl))
            root.destroy.assert_called_once()

    def test_first_run_cancel_does_not_create_settings(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "settings.json"
            with patch.object(config, "SETTINGS_FILE", file_path), \
                 patch.object(scheduler, "load_settings", side_effect=config.load_settings), \
                 patch.object(scheduler.tk, "Tk"), \
                 patch.object(scheduler.messagebox, "showinfo"), \
                 patch.object(scheduler.filedialog, "askopenfilename", return_value=""):
                scheduler.main()
            self.assertFalse(file_path.exists())

    def test_both_sdl_time_types_generate_calendar_entries(self):
        with tempfile.TemporaryDirectory() as directory:
            for time_type in ("0", "1"):
                with self.subTest(time_type=time_type):
                    path = Path(directory) / f"schedule-{time_type}.sdl"
                    path.write_text(
                        "[event0]\nEnabledEvent=1\nTaskName=Test\n"
                        "DateTime=2026-01-01 10:00:00\n"
                        "UseDate=0\nUseDaysOfWeek=1\nDays=1111111\n"
                        f"TimeType={time_type}\n"
                        "Hours=000000000010000000000000\nMinutes=00\nSeconds=0\n",
                        encoding="utf-8",
                    )
                    events = Database({"admin_sdl": str(path)}).load_events()
                    self.assertEqual(len(events), 1)
                    self.assertGreater(len(SchedulerController(events).refresh()), 0)


if __name__ == "__main__":
    unittest.main()
