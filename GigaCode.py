'''
Summary
GigaCode Functions for Function Database
'''
import os
import re
import json

# Main Classes
class Function:
    def __init__(self, name, params, desc, imports, code):
        self.name = name
        self.params = params
        self.desc = desc
        self.imports = imports
        self.code = code
    
    def getCode(self):
        codeText = ''

        # Name and Params
        codeText = "def " + self.name + "(" + self.params + "):"
        codeText = codeText + "\n"

        # Desc
        for dl in self.desc:
            codeText = codeText + "    # " + dl
            codeText = codeText + "\n"

        codeText = codeText + "\n"

        # Imports
        for il in self.imports:
            codeText = codeText + "    " + il
            codeText = codeText + "\n"

        codeText = codeText + "\n"

        # Code
        for cl in self.code:
            codeText = codeText + "    " + cl
            codeText = codeText + "\n"

        codeText.rstrip('\n')
        
        return codeText

# Main Functions
def ExtractPythonFunctions(data=None, file_path='', formatJSONPath='Format_Python_Standard.json', tabSpace=4):
    ''' Extracts Functions (NOT CLASS FUNCTIONS) from a python file '''
    Functions = []

    FormatParams = json.load(open(formatJSONPath, 'rb'))

    # Read Text of File
    if data == None:
        data = open(file_path, 'r').read()
    
    file_text = data

    # Replace all tabs by appropriate spaces
    file_text.replace('\t', ' ' * tabSpace)

    # Split by \n
    code_lines = file_text.split('\n')

    # Loop thru lines and identify functions
    inFunc = False
    inDesc = False
    DescFound = False
    inImports = False
    curFunc = {"name": '', "params": '', "desc": [], "imports": [], "code": []}
    for line in code_lines:
        line_stripped = line.strip()
        if line_stripped == '':
            continue

        # Function Start Check
        if not inFunc and FormatParams['ID_FuncStart'] == line_stripped:
            inFunc = True
            continue
        # Function End Check
        elif inFunc and FormatParams['ID_FuncEnd'] == line_stripped:
            inFunc = False
            inDesc = False
            DescFound = False
            inImports = False
            f = Function(curFunc['name'], curFunc['params'], curFunc['desc'], curFunc['imports'], curFunc['code'])
            Functions.append(f)
            curFunc = {"name": '', "params": '', "desc": [], "imports": [], "code": []}
            continue
        # In Function
        if inFunc:
            # Desc Check
            if not DescFound:
                # Desc Start Check
                if not inDesc and FormatParams['ID_DescStart'] == line_stripped:
                    inDesc = True
                    continue
                # Desc End Check
                elif inDesc and FormatParams['ID_DescEnd'] == line_stripped:
                    inDesc = False
                    DescFound = True
                    continue
                # In Desc
                elif inDesc:
                    if line_stripped.startswith(FormatParams['Strip_DescStart']):
                        line_stripped = line_stripped[len(FormatParams['Strip_DescStart']):].strip()
                    curFunc['desc'].append(line_stripped)
                    continue
            # Imports Start Check
            if not inImports and FormatParams['ID_ImportsStart'] == line_stripped:
                inImports = True
                continue
            # Imports End Check
            elif inImports and FormatParams['ID_ImportsEnd'] == line_stripped:
                inImports = False
                continue
            # In Imports
            elif inImports:
                curFunc['imports'].append(line_stripped)
                continue
            else:
                # Function Name and Params
                if len(re.findall(FormatParams['Data_FuncName'], line_stripped)) > 0:
                    curFunc['name'] = re.findall(FormatParams['Data_FuncName'], line_stripped)[0].strip()
                    curFunc['params'] = (re.findall(FormatParams['Data_FuncParams'], line_stripped)[0].strip())
                # Code
                else:
                    linedata = line.rstrip()
                    if line.startswith(' '*tabSpace):
                        linedata = line[tabSpace:]
                    curFunc['code'].append(linedata)

    Functions_dict = []
    for f in Functions:
        fd = {"Name": f.name, "Description": f.desc, "Imports": f.imports, "Parameters": f.params, "Code": f.getCode().split('\n')}
        Functions_dict.append(fd)
    return Functions_dict



# Driver Code
# Functions = ExtractPythonFunctions(file_path='Code/Python/Test.py', formatJSONPath='Format_Python_Standard.json', tabSpace=4)
# # import pickle
# # Functions = pickle.load(open('FunctionDatabases/PythonTestDB.p', 'rb'))
# for f in Functions:
#     print('\n\n')
#     print("Name:", f.name)
#     print("Desc:", f.desc)
#     print("Imports:", f.imports)
#     print("Parameters:", f.params)
#     print("CodeLines:", f.code)
#     print("Code:\n", f.getCode())