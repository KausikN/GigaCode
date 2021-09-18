import os
import re
import json

import functools
import inspect
import importlib
import ast

# Main Classes


# Main Functions
def ParseFunction_Python_Regex(code, tabSpace=4):
    ''' Parses python function code '''

    # Regex
    Regex_FuncName = "^.*def([^(]*)\\("
    Regex_ParamsOneLine = "^.*def[^(]*\\((.*)\\)"

    # Init
    FunctionData = {"name": '', "params": '', "desc": [], "imports": [], "code": []}

    # Replace all tabs by appropriate spaces
    code = code.replace('\t', ' ' * tabSpace)

    # Split by \n
    code_lines = code.split('\n')

    # Loop thru lines and identify functions
    inFunc = False
    
    for line in code_lines:
        line_stripped = line.strip()
        if line_stripped == '' or line_stripped.startswith('#'):
            continue

        # Function Start Check
        if not inFunc:
            if line_stripped.startswith('def '):
                inFunc = True
                FuncNameRegexMatches = re.findall(Regex_FuncName, line_stripped)
                if len(FuncNameRegexMatches) > 0:
                    FunctionData['name'] = FuncNameRegexMatches[0].strip()
                    if line_stripped.endswith('):'):
                        ParamsRegexMatches = re.findall(Regex_ParamsOneLine, line_stripped)
                        if len(ParamsRegexMatches) > 0: FunctionData['params'] = FuncNameRegexMatches[0].strip()
                continue

        # In Function
        if inFunc:
            # Code
            linedata = line.rstrip()
            FunctionData['code'].append(linedata)

    return FunctionData

# Using Compilers
def AST_FunctionDataExtract(f, fullCode):
    ''' Extracts function data from AST '''

    # Init
    FunctionData = {"language": "python", "name": '', "params": '', "desc": "", "imports": [], "code": ""}

    # Extract
    # Name
    FunctionData['name'] = f.name

    # Desc
    # FunctionData['desc'] = [x.s for x in f.body]

    # Imports
    ImportsData = []
    Imports = [x for x in f.body if isinstance(x, ast.Import)]
    FromImports = [x for x in f.body if isinstance(x, ast.ImportFrom)]
    for impG in Imports:
        impsDicts = []
        for imp in impG.names:
            name = imp.name.split(".")[-1]
            module = imp.name.rstrip(name).rstrip(".")
            impData = {
                "name": name,
                "dependency_path": module.split(".")
            }
            impsDicts.append(impData)
        ImportsData.extend(impsDicts)
    for impG in FromImports:
        impsDicts = []
        for imp in impG.names:
            name = imp.name.split(".")[-1]
            module = ".".join([impG.module, imp.name.rstrip(name).rstrip(".")]).rstrip(".")
            impData = {
                "name": name,
                "dependency_path": module.split(".")
            }
            impsDicts.append(impData)
        ImportsData.extend(impsDicts)
    FunctionData['imports'] = ImportsData

    # Params
    FunctionData['params'] = []
    defaultCount = len(f.args.defaults)
    argsCount = len(f.args.args)
    for i in range(len(f.args.args)):
        a = f.args.args[i]
        d = None
        if i >= argsCount - defaultCount:
            d = f.args.defaults[i - (argsCount - defaultCount)].value
        d_dict = {"value": d}
        t = a.annotation.id if a.annotation is not None else None
        paramData = {
            "name": a.arg,
            "desc": "",
            "default_value": json.dumps(d_dict),
            "type": t
        }
        FunctionData['params'].append(paramData)

    # Code
    FunctionData['code'] = ast.get_source_segment(fullCode, f)

    return FunctionData

def ParseFunction_Python_Compiler(code):
    ''' Parses python function code using compiler '''

    CodeModule = ast.parse(code)

    functions = [x for x in CodeModule.body if isinstance(x, ast.FunctionDef)]

    functions_data = [AST_FunctionDataExtract(f, code) for f in functions]

    return functions_data

# Driver Code
# Params
filePath = "Parsers/TestPython.py"
# Params

# RunCode
# Read Code
code = open(filePath, 'r').read()

# Parse
FunctionData = ParseFunction_Python_Compiler(code)

# Print
FunctionData = {"Funcs": FunctionData}
savePath = os.path.splitext(filePath)[0] + "_Funcs.json"
json.dump(FunctionData, open(savePath, 'w'), indent=4)