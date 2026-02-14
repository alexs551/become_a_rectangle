# LOCALLY installs pygame to your folder
# Does not work with 3.14 and above.
import subprocess
import sys

path = "" # IMPORTANT - PLEASE READ: replace "" with the path to the folder with "main.py" and use / instead of \

def install(path):
    print("Installing pygame. This may take a while.")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame", "-t", path])
        print("Successful install. You can now run \"main.py\"")
    except:
        print("There was an error installing. Please try running the script again.")


install(path)

