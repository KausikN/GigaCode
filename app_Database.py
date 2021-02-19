'''
Summary
Add to Database App for GigaCode Function Database for Python Codes
'''
import GigaCode

import os
import json
import tkinter as tk
from tkinter import *
import pickle
from tqdm import tqdm
from PIL import ImageTk, Image
from tkinter import filedialog

curRow = 0
MainLabelText_DB = None
NFilesLabelText_DB = None
FileLabels_DB = []
DBFile_Text = None
DBNameTextField = None

DBFile_Path = ''

config = json.load(open('config.json', 'rb'))


# Utils


# TKinter Window
def CreateWindow():
    global curRow
    global MainLabelText_DB
    global NFilesLabelText_DB
    global DBNameTextField
    global DBFile_Text

    Button(root, text="Select File", command=SelectFileDialogBox_File).grid(row=curRow, column=0)
    Button(root, text="Add to Database", command=Add2DB).grid(row=curRow, column=1)
    Button(root, text="Remove Last File", command=RemoveLastFile_DB).grid(row=curRow, column=2)
    curRow += 1
    Button(root, text="Select DB File", command=SelectFileDialogBox_DBFile).grid(row=curRow, column=0)
    Button(root, text="Create DB File", command=SelectFileDialogBox_CreateDBFile).grid(row=curRow, column=1)
    curRow += 1
    MainLabelText_DB = tk.StringVar()
    MainLabelText_DB.set("")
    MainLabel_DB = Label(root, textvariable=MainLabelText_DB)
    MainLabel_DB.grid(row=curRow, column=0)
    curRow += 1
    NFilesLabelText_DB = tk.StringVar()
    NFilesLabelText_DB.set("No Files Added")
    NFilesLabel_DB = Label(root, textvariable=NFilesLabelText_DB)
    NFilesLabel_DB.grid(row=curRow, column=0)
    curRow += 1
    DBFile_Text = tk.StringVar()
    DBFile_Text.set("No Files Added")
    DBFile_Label = Label(root, textvariable=DBFile_Text)
    DBFile_Label.grid(row=curRow, column=0)
    curRow += 1
    DBNameLabel = Label(root, text="DB Name: ")
    DBNameLabel.grid(row=curRow, column=0)
    DBNameTextField = Entry(root)
    DBNameTextField.grid(row=curRow, column=1)
    curRow += 1

def SelectFileDialogBox_File():
    global curRow
    global FileLabels_DB
    global MainLabelText_DB
    global NFilesLabelText_DB
    global OpenedFiles

    # Create File Dialog Box
    root.filenames = filedialog.askopenfilenames(initialdir='./', title="Select Files")

    MainLabelText_DB.set("")

    for filename in root.filenames:
        if not filename in OpenedFiles:
            OpenedFiles.append(filename)
            NFilesLabelText_DB.set("Added " + str(len(OpenedFiles)) + " Files")
            newfilelabel = Label(root, text=filename)
            newfilelabel.grid(row=curRow, column=1)
            FileLabels_DB.append(newfilelabel)
            curRow += 1
        else:
            MainLabelText_DB.set("File already added.")

def SelectFileDialogBox_DBFile():
    global curRow
    global DBFile_Path
    global DBFile_Text
    global MainLabelText_DB

    # Create File Dialog Box
    root.filename = filedialog.askopenfilename(initialdir='./', title="Select DB File")

    MainLabelText_DB.set("")

    if not os.path.splitext(root.filename)[-1] == '.p': # Check if selected file is json
        MainLabelText_DB.set("Please select a proper pickle File.")
        return
    else:
        DBFile_Text.set('DB File: ' + root.filename)
        DBFile_Path = root.filename

def SelectFileDialogBox_CreateDBFile():
    global curRow
    global DBFile_Path
    global DBFile_Text
    global DBNameTextField
    global MainLabelText_DB

    # Create File Dialog Box
    root.dirname = filedialog.askdirectory(initialdir='./', title="Select DB File Dir")

    MainLabelText_DB.set("")

    DBFile_Path = os.path.join(root.dirname, str(DBNameTextField.get()))

    pickle.dump([], open(DBFile_Path, 'wb'))

    DBFile_Text.set('DB File: ' + DBFile_Path)

    MainLabelText_DB.set("Created DBFile " + str(DBNameTextField.get()) + " at " + root.dirname)    

def Add2DB():
    global OpenedFiles
    global DBFile_Path

    if not len(OpenedFiles) == 0:
        MainLabelText_DB.set("Adding Functions...")
        Functions = pickle.load(open(DBFile_Path, 'rb'))
        if Functions == None:
            Functions = []
        for filepath in tqdm(OpenedFiles):
            Functions.extend(GigaCode.ExtractPythonFunctions(file_path=filepath, formatJSONPath=config['PythonFormatPath'], tabSpace=config['tabSpace']))
        pickle.dump(Functions, open(DBFile_Path, 'wb'))
        MainLabelText_DB.set("Finished Adding Functions")
    else:
        MainLabelText_DB.set("Please select atleast one valid Image file to upload.")

def RemoveLastFile_DB():
    global OpenedFiles
    global FileLabels_DB
    global NFilesLabelText_DB

    if len(OpenedFiles) > 0:
        OpenedFiles.pop()
        FileLabels_DB[-1].grid_forget()
        FileLabels_DB.pop()
        if len(OpenedFiles) > 0:
            NFilesLabelText_DB.set("Added " + str(len(OpenedFiles)) + " Directories")
        else:
            NFilesLabelText_DB.set("No Dir Added")



# Main Code

# Details
OpenedFiles = []

# Init Root
print('Creating Window...')
root = Tk()
root.title('GigaCode Database App')

# Create Window
CreateWindow()
print('Created Window')

root.mainloop()