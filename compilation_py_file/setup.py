from cx_Freeze import setup, Executable
import os,sys
os.environ['TCL_LIBRARY'] = r'C:\Users\username\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\username\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'
build_exe_options = {"packages": ["os"], "excludes": ["PyQt5"]}
sys.argv.append("build")
filename = "text.py" # Youre file name python 
base = None
if sys.platform == "win32":
    base = "Win32GUI"
setup(
    name = "names",
    version = "0.1",
    description = "title",
    executables = [Executable(filename, base=base)])
