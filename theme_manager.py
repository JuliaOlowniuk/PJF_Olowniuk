from tkinter import ttk

def set_light_theme():
    theme = ttk.Style()
    theme.theme_use('clam')
    theme.configure('.', background='#d9d9d9', foreground='black')

def set_dark_theme():
    theme = ttk.Style()
    theme.theme_use('clam')
    theme.configure('.', background='#2d2d2d', foreground='white')
