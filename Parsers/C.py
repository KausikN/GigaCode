import os
import re
import json

import functools
import inspect
import importlib
import ast
import pycparser

# Main Classes


# Main Functions
def ParseFunction_C_Regex(code):
    ''' Parses C function code '''

    FunctionData = {}

    return FunctionData

# Using Compilers
def AST_GetType(obj):
    t = None
    t_t = obj
    while True:
        if "type" in t_t.__dir__():
            t_t = t_t.type
        else:
            t = t_t.names
            break
    return t

def AST_FunctionDataExtract(f, fullCode):
    ''' Extracts function data from AST '''

    # Init
    FunctionData = {"language": "c", "name": '', "params": {}, "desc": "", "imports": [], "code": "", "return": {}}

    # Extract
    # Name
    FunctionData['name'] = f.decl.name

    # Desc
    # FunctionData['desc'] = [x.s for x in f.body]

    # Imports
    ImportsData = []
    FunctionData['imports'] = ImportsData

    # Params
    FunctionData['params'] = []
    if f.decl.type.args is not None:
        params = f.decl.type.args.params
        for i in range(len(params)):
            param = params[i]
            d = param.init
            d_dict = {"value": d}
            t = AST_GetType(param.type)
            paramData = {
                "name": param.name,
                "desc": "",
                "default_value": json.dumps(d_dict),
                "type": t
            }
            FunctionData['params'].append(paramData)

    # Code
    FunctionData['code'] = ast.get_source_segment(fullCode, f)

    # Return
    FunctionData['return'] = {
        "type": AST_GetType(f.decl)
    }

    return FunctionData

def ParseFunction_C_Compiler(filePath):
    ''' Parses C function code using compiler '''

    CodeModule = pycparser.parse_file(filename=filePath)
    Code = open(filePath, 'r').read()

    functions = [fd[1] for fd in CodeModule.children()]

    functions_data = [AST_FunctionDataExtract(f, Code) for f in functions]

    return functions_data

# Driver Code
# Params
filePath = "Parsers/TestC.c"
# Params

# RunCode
# Parse
FunctionData = ParseFunction_C_Compiler(filePath)

# Print
FunctionData = {"Funcs": FunctionData}
savePath = os.path.splitext(filePath)[0] + "_Funcs.json"
json.dump(FunctionData, open(savePath, 'w'), indent=4)