'''
Summary
Main app for viewing database of functions
'''

import os
import tkinter as tk
from tkinter import *
import pickle
from tqdm import tqdm
from PIL import ImageTk, Image
from tkinter import filedialog

curRow = 0

MainLabelText_DB = None
FunctionNameTextField = None
FunctionDetailsText = None
DBFile_Path = ''

Functions = None
FunctionHashMap = None


# Utils


# TKinter Window
def CreateWindow():
    global curRow
    global MainLabelText_DB
    global FunctionNameTextField
    global FunctionDetailsText

    Button(root, text="Select DB File", command=SelectFileDialogBox_DBFile).grid(row=curRow, column=0)
    Button(root, text="Search Function", command=SearchFunctions).grid(row=curRow, column=1)
    curRow += 1
    MainLabelText_DB = tk.StringVar()
    MainLabelText_DB.set("")
    MainLabel_DB = Label(root, textvariable=MainLabelText_DB)
    MainLabel_DB.grid(row=curRow, column=1)
    curRow += 1
    FunctionNameLabel = Label(root, text="Function Name: ")
    FunctionNameLabel.grid(row=curRow, column=0)
    FunctionNameTextField = Entry(root)
    FunctionNameTextField.grid(row=curRow, column=1)
    curRow += 1
    FunctionDetailsText = tk.StringVar()
    FunctionDetailsText.set("")
    FunctionDetailsLabel = Label(root, textvariable=FunctionDetailsText)
    FunctionDetailsLabel.grid(row=curRow, column=1)
    curRow += 1

def SelectFileDialogBox_DBFile():
    global curRow
    global MainLabelText_DB
    global DBFile_Path
    global Functions
    global FunctionHashMap

    # Create File Dialog Box
    root.filename = filedialog.askopenfilename(initialdir='./', title="Select DB File")

    MainLabelText_DB.set("")

    if not os.path.splitext(root.filename)[-1] == '.p': # Check if selected file is pickle
        MainLabelText_DB.set("Please select a proper pickle File.")
        return
    else:
        MainLabelText_DB.set('DB File: ' + root.filename)
        DBFile_Path = root.filename
        Functions = pickle.load(open(DBFile_Path, 'rb'))
        FunctionHashMap = GenerateFunctionHashMap(Functions)

def SearchFunctions():
    global FunctionNameTextField
    global FunctionDetailsText
    global FunctionHashMap

    if FunctionHashMap == None:
        FunctionDetailsText.set("Select a DB File First")
        return

    RequiredFunctionName = str(FunctionNameTextField.get()).strip()
    FunctionsDetails = ""

    if RequiredFunctionName in FunctionHashMap.keys():
        fi = 1
        for f in FunctionHashMap[RequiredFunctionName]:
            FunctionsDetails += str(fi) + ") " + "\n"
            FunctionsDetails += "Name: " + f['Name'] + "\n"
            FunctionsDetails += "Desc: " + f['Description'] + "\n"
            FunctionsDetails += "Para: " + ', '.join(f['Parameters']) + "\n\n"
            FunctionsDetails += '\n'.join(f['Code']) + "\n\n"
            fi += 1
        FunctionDetailsText.set(FunctionsDetails)
    else:
        FunctionDetailsText.set("No Functions of that Name")
    

def GenerateFunctionHashMap(Functions):
    FunctionHashMap = {}

    for f in Functions:
        if not f['Name'] in FunctionHashMap.keys():
            FunctionHashMap[f['Name']] = []
        FunctionHashMap[f['Name']].append(f)
    
    return FunctionHashMap

# Main Code

# Details
OpenedFiles = []

# Init Root
print('Creating Window...')
root = Tk()
root.title('GigaCode Function Search')

# Create Window
CreateWindow()
print('Created Window')

root.mainloop()