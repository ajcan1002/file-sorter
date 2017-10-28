# file-sorter
Program to sort files by file extension into different folders

# GUI.py
User interface class. Provides a GUI that allows the user to easily edit the program data. Will write all user-inputted information to the config.ini file, which is then parsed and read by mover.py

# mover.py
The actual program file. Pulls information from config.ini and then moves files accordingly using shutil. Can be continuously run in background if looping is set to true.
