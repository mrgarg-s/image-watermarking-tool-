"""
Light UI launcher for the existing Secure Watermarking Software.

This keeps the watermarking, encryption, PDF, batch, undo/redo, drag-and-drop,
and export logic unchanged. It only remaps the existing Tkinter dark colors to
an airy light-blue/white visual theme at runtime.

Run:
    python "Light UI Launcher.py"
"""
import importlib.util
import os
import tkinter as tk
from tkinter import ttk

# Modern light palette
LIGHT = {
    "#121212": "#F5F7FB",
    "#1e1e1e": "#FFFFFF",
    "#ffffff": "#172033",
    "#BB86FC": "#2563EB",
    "#333333": "#E8EEF7",
    "#2b2b2b": "#EAF0F8",
    "#444444": "#D5DFEE",
    "#000000": "#EEF4FF",
    "#202020": "#FFFFFF",
    "#666666": "#667085",
    "#888888": "#667085",
    "#03DAC6": "#2563EB",
}


def color(value):
    if isinstance(value, str):
        return LIGHT.get(value.lower(), value)
    return value


# Translate direct Tkinter widget colors, including root.configure().
_original_configure = tk.Misc.configure
_original_config = tk.Misc.config


def light_configure(self, cnf=None, **kw):
    if cnf:
        cnf = dict(cnf)
        for key in ("bg", "background", "fg", "foreground", "insertbackground", "highlightbackground"):
            if key in cnf:
                cnf[key] = color(cnf[key])
    for key in ("bg", "background", "fg", "foreground", "insertbackground", "highlightbackground"):
        if key in kw:
            kw[key] = color(kw[key])
    return _original_configure(self, cnf, **kw)


def light_config(self, cnf=None, **kw):
    return light_configure(self, cnf, **kw)


tk.Misc.configure = light_configure
tk.Misc.config = light_config

# Translate colors supplied directly to Tk widget constructors.
def wrap_widget(cls):
    original = cls

    def factory(*args, **kwargs):
        for key in ("bg", "background", "fg", "foreground", "insertbackground", "highlightbackground"):
            if key in kwargs:
                kwargs[key] = color(kwargs[key])
        return original(*args, **kwargs)

    return factory


for _name in (
    "Frame", "Label", "Button", "Canvas", "PanedWindow", "Entry", "Text",
    "Checkbutton", "Radiobutton", "Scale", "Spinbox", "Listbox", "Message"
):
    if hasattr(tk, _name):
        setattr(tk, _name, wrap_widget(getattr(tk, _name)))

# Translate ttk style colors used by the existing application.
_original_style_configure = ttk.Style.configure
_original_style_map = ttk.Style.map


def light_style_configure(self, style, query_opt=None, **kw):
    if query_opt is not None:
        query_opt = {k: color(v) for k, v in query_opt.items()}
    kw = {k: color(v) for k, v in kw.items()}
    return _original_style_configure(self, style, query_opt, **kw)


def light_style_map(self, style, query_opt=None, **kw):
    if query_opt is not None:
        query_opt = {k: color(v) for k, v in query_opt.items()}
    if kw:
        kw = {k: color(v) for k, v in kw.items()}
    return _original_style_map(self, style, query_opt, **kw)


ttk.Style.configure = light_style_configure
ttk.Style.map = light_style_map

# Load the original application without changing its functional code.
APP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Watermark software.py")
spec = importlib.util.spec_from_file_location("watermark_original", APP_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# The original file contains its own __main__ block, so start the same app here.
if getattr(module, "HAS_DND", False):
    root = module.TkinterDnD.Tk()
else:
    root = tk.Tk()
    print("Warning: tkinterdnd2 missing. Drag and drop disabled.")

app = module.WaterMarkProjectApp(root)
root.mainloop()
