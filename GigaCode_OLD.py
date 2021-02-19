'''
Summary
GigaCode Functions for Function Database
'''
import os
import re

def ExtractFunctionsFromFile_Python(file_path='', file_obj=None, tabSpace=4):
    ''' Extracts Functions (NOT CLASS FUNCTIONS) from a python file '''
    Functions = []

    # Read Text of File
    if file_obj == None:
        file_obj = open(file_path, 'r')
    
    file_text = file_obj.read()

    # As Python Split by \n
    code_lines = file_text.split('\n')

    # Loop and identify functions
    tabAlernateSpaces = ' ' * tabSpace
    InFunction = False
    InFunctionDesc = None
    curFunctionName = ''
    curFunctionParams = []
    curFunctionLines = []
    curFunctionDesc = ''
    for line in code_lines:
        if InFunction:
            # Check if Description Line
            stripped_line = re.findall('^\t*(.*)', line.strip())[0]
            if not InFunctionDesc == None:
                if stripped_line.endswith(InFunctionDesc):
                    InFunctionDesc = None
                    curFunctionDesc += stripped_line[:-3]
                    continue
                else:
                    curFunctionDesc += line
                    continue

            if stripped_line.startswith("'''"):
                InFunctionDesc = "'''"
                curFunctionDesc += stripped_line[3:]
                stripped_line = stripped_line[3:]
                if stripped_line.endswith(InFunctionDesc):
                    InFunctionDesc = None
                    curFunctionDesc = curFunctionDesc[:-3]
                continue
            elif stripped_line.startswith('"""'):
                InFunctionDesc = '"""'
                curFunctionDesc += stripped_line[3:]
                stripped_line = stripped_line[3:]
                if stripped_line.endswith(InFunctionDesc):
                    InFunctionDesc = None
                    curFunctionDesc = curFunctionDesc[:-3]
                continue


            # If Starting with tab space or empty line then it is within the function
            # If Comment always add to function code lines
            if line.strip() == '' or (line.startswith('\t') or line.startswith(tabAlernateSpaces)) or not re.search('^#.*', line.strip()) == None:
                #print("curapp:", line)
                curFunctionLines.append(line)
                continue
            # If not starting with tab or comment or empty, end function lines
            else:
                #print("curclose:", line)
                curFunction = {}
                curFunction['Name'] = curFunctionName.strip()
                curFunction['Parameters'] = curFunctionParams
                curFunction['Code'] = curFunctionLines
                curFunction['Description'] = curFunctionDesc.strip()
                Functions.append(curFunction)
                curFunctionName = ''
                curFunctionParams = []
                curFunctionLines = []
                curFunctionDesc = ''
                InFunction = False
        # If starting with def, new function
        if line.startswith('def'):
            #print("funcstart:", line)
            InFunction = True
            curFunctionName = ''
            curFunctionParams = []
            curFunctionLines = []
            curFunctionDesc = ''
            curFunctionLines.append(line)
            # Find name and parameters of function
            curFunctionName = re.findall('^def([^(]*)\(', line.strip())[0].strip()
            curFunctionParams = (re.findall('^def[^(]*\((.*)\)', line.strip())[0].strip()).split(',')
            for pi in range(len(curFunctionParams)):
                curFunctionParams[pi] = curFunctionParams[pi].strip()

    return Functions


class PythonParams:
    def __init__(self):
        self.DescriptionMarks_Start = ['"""', "'''"]
        self.DescriptionMarks_End = ['"""', "'''"]
        self.CommentRegeX = '^#.*'
        self.FunctionNameRegeX = '^def([^(]*)\('
        self.FunctionParamsRegeX = '^def[^(]*\((.*)\)'
        self.tabAlernateSpaces = ' ' * 4
    
    def InFunctionBlockCheck(self, line):
        return (line.startswith('\t') or line.startswith(self.tabAlernateSpaces))

    def NewFunctionCheck(self, line):
        return line.startswith('def')


def GetLanguageParams(language):
    params = None
    if language == 'Python':
        params = PythonParams()
        return params


def ExtractFunctionsFromFile(file_path='', file_obj=None, language='Python', tabSpace=4):
    ''' Extracts Functions (NOT CLASS FUNCTIONS) from a python file '''
    Functions = []

    LanguageParams = GetLanguageParams(language)

    # Read Text of File
    if file_obj == None:
        file_obj = open(file_path, 'r')
    
    file_text = file_obj.read()

    # Split by \n
    code_lines = file_text.split('\n')

    # Loop and identify functions
    tabAlernateSpaces = ' ' * tabSpace
    LanguageParams.tabAlernateSpaces = tabAlernateSpaces
    InFunction = False
    InFunctionDescEnd = None
    curFunctionName = ''
    curFunctionParams = []
    curFunctionLines = []
    curFunctionDesc = ''
    for line in code_lines:
        if InFunction:
            # Check if Description Line
            stripped_line = re.findall('^\t*(.*)', line.strip())[0]
            if not InFunctionDescEnd == None:
                if stripped_line.endswith(InFunctionDescEnd):
                    InFunctionDescEnd = None
                    curFunctionDesc += stripped_line[:-len(InFunctionDescEnd)]
                    continue
                else:
                    curFunctionDesc += line
                    continue
            
            MarkCheck = False
            for descmarkstart, descmarkend in zip(LanguageParams.DescriptionMarks_Start, LanguageParams.DescriptionMarks_End):
                if stripped_line.startswith(descmarkstart):
                    InFunctionDescEnd = descmarkend
                    curFunctionDesc += stripped_line[len(descmarkstart):]
                    stripped_line = stripped_line[len(descmarkstart):]
                    if stripped_line.endswith(InFunctionDescEnd):
                        InFunctionDescEnd = None
                        curFunctionDesc = curFunctionDesc[:-len(descmarkstart)]
                    MarkCheck = True
                    break
            if MarkCheck:
                continue

            # Check if in function block
            # If Comment always add to function code lines
            if line.strip() == '' or (LanguageParams.InFunctionBlockCheck(line)) or not re.search(LanguageParams.CommentRegeX, line.strip()) == None:
                #print("curapp:", line)
                curFunctionLines.append(line)
                continue
            # If not within function block, end function lines
            else:
                #print("curclose:", line)
                curFunction = {}
                curFunction['Name'] = curFunctionName.strip()
                curFunction['Parameters'] = curFunctionParams
                curFunction['Code'] = curFunctionLines
                curFunction['Description'] = curFunctionDesc.strip()
                Functions.append(curFunction)
                curFunctionName = ''
                curFunctionParams = []
                curFunctionLines = []
                curFunctionDesc = ''
                InFunction = False
        # New function check
        if LanguageParams.NewFunctionCheck(line):
            #print("funcstart:", line)
            InFunction = True
            curFunctionName = ''
            curFunctionParams = []
            curFunctionLines = []
            curFunctionDesc = ''
            curFunctionLines.append(line)
            # Find name and parameters of function
            curFunctionName = re.findall(LanguageParams.FunctionNameRegeX, line.strip())[0].strip()
            curFunctionParams = (re.findall(LanguageParams.FunctionParamsRegeX, line.strip())[0].strip()).split(',')
            for pi in range(len(curFunctionParams)):
                curFunctionParams[pi] = curFunctionParams[pi].strip()

    return Functions



# Driver Code
Functions = ExtractFunctionsFromFile('GigaCode.py', language='Python', tabSpace=4)
# import pickle
# Functions = pickle.load(open('FunctionDatabases/PythonTestDB.p', 'rb'))
for f in Functions:
    print('\n\n')
    print("Name:", f['Name'])
    print("Desc:", f['Description'])
    print("Parameters:", f['Parameters'])
    for fl in f['Code']:
        print(fl)