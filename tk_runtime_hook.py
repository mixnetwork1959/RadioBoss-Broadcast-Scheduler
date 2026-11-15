"""Set Tcl/Tk resource paths before tkinter is imported in the frozen app."""

import os
import sys
from pathlib import Path


def configure_tk_paths():
    bundle_root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    for variable, subfolder, required in (
        ("TCL_LIBRARY", "_tcl_data", "init.tcl"),
        ("TK_LIBRARY", "_tk_data", "tk.tcl"),
    ):
        resource_dir = bundle_root / subfolder
        if (resource_dir / required).is_file():
            os.environ[variable] = str(resource_dir)


configure_tk_paths()
