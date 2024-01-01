import tkinter as tk
from tkinter import ttk
def set_light_theme(root):
    root.option_add('*TButton*highlightBackground', '#d9d9d9')
    root.option_add('*TButton*highlightColor', 'SystemButtonFace')
    root.option_add('*TButton*background', '#d9d9d9')
    root.option_add('*TButton*foreground', 'black')
    root.option_add('*TButton*borderWidth', 2)
    root.option_add('*TButton*relief', 'flat')

    root.option_add('*TLabel*background', '#d9d9d9')
    root.option_add('*TLabel*foreground', 'black')

    root.option_add('*TEntry*background', 'white')
    root.option_add('*TEntry*foreground', 'black')

    root.option_add('*TListbox*background', 'white')
    root.option_add('*TListbox*foreground', 'black')

def set_dark_theme(root):
    root.option_add('*TButton*highlightBackground', '#2d2d2d')
    root.option_add('*TButton*highlightColor', '#2d2d2d')
    root.option_add('*TButton*background', '#2d2d2d')
    root.option_add('*TButton*foreground', 'white')
    root.option_add('*TButton*borderWidth', 2)
    root.option_add('*TButton*relief', 'flat')

    root.option_add('*TLabel*background', '#2d2d2d')
    root.option_add('*TLabel*foreground', 'white')

    root.option_add('*TEntry*background', '#4d4d4d')
    root.option_add('*TEntry*foreground', 'white')

    root.option_add('*TListbox*background', '#4d4d4d')
    root.option_add('*TListbox*foreground', 'white')
