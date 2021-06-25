"""
Stream lit GUI for hosting GigaCode
"""

# Imports
import os
import base64
import streamlit as st
import json

import GigaCode

# Main Vars
config = json.load(open('./StreamLitGUI/UIConfig.json', 'r'))

# Main Functions
def main():
    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    'Choose one of the following',
        tuple(
            [config['PROJECT_NAME']] + 
            config['PROJECT_MODES']
        )
    )

    # Custom Code for this REPO -- DO NOT USE FOR ANY OTHER PROJECT
    if not (selected_box == "Function Database"):
        ResetRemovedList()
    
    if selected_box == config['PROJECT_NAME']:
        HomePage()
    else:
        correspondingFuncName = selected_box.replace(' ', '_').lower()
        if correspondingFuncName in globals().keys():
            globals()[correspondingFuncName]()
 

def HomePage():
    st.title(config['PROJECT_NAME'])
    st.markdown('Github Repo: ' + "[" + config['PROJECT_LINK'] + "](" + config['PROJECT_LINK'] + ")")
    st.markdown(config['PROJECT_DESC'])

    # st.write(open(config['PROJECT_README'], 'r').read())

#############################################################################################################################
# Repo Based Vars
DEFAULT_DATABASE_SAVEPATH = 'FunctionDatabases/Cache/FunctionsDatabase.json'
DEFAULT_REMOVEDFUNCTIONS_CACHEPATH = 'FunctionDatabases/Cache/RemovedFunctions.txt'

PARSER_FORMATS = {
    "Python" : {
        "Python - Standard": "Formats/Format_Python_Standard.json"
    },
    "C": {},
    "Verilog": {}
}

DATABASES = {
    "Python": [
        {
            "name": "Python Functions Volume 1",
            "path" : "FunctionDatabases/PythonFunctions_NEW.json"
        }
    ],
    "C": [],
    "Verilog": []
}

FUNCTIONS = {
    "Python": [],
    "C": [],
    "Verilog": []
}

# Util Vars
FUNCTIONS_HASHMAP = None

# Util Functions
def GetFunctionDisplayNames(functions):
    functions_dns = []
    for f in functions:
        functions_dns.append(f['Name'] + "(" + f['Parameters'] + ")")
    return functions_dns

def DownloadFile(filePath, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    object_to_download = open(filePath, 'r').read()
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def ResetRemovedList():
    open(DEFAULT_REMOVEDFUNCTIONS_CACHEPATH, 'w').write("")

def GetRemovedFunctions(functions):
    RemovedFunctionsData = open(DEFAULT_REMOVEDFUNCTIONS_CACHEPATH, 'r').read()
    print("READ Removed Cache:", RemovedFunctionsData)
    if RemovedFunctionsData.strip() == "": return functions, [], list(range(len(functions))), []
    RemovedFunctionsIndices = list(map(int, RemovedFunctionsData.split(",")))
    RemovedFunctions = []
    AddedFunctions = []
    AddedFunctionsIndices = []
    for i in range(len(functions)):
        if i in RemovedFunctionsIndices:
            RemovedFunctions.append(functions[i])
        else:
            AddedFunctions.append(functions[i])
            AddedFunctionsIndices.append(i)
    return AddedFunctions, RemovedFunctions, AddedFunctionsIndices, RemovedFunctionsIndices

def SetRemovedFunctions(RemovedIndices):
    RemovedIndices_Text = ','.join(list(map(str, RemovedIndices)))
    open(DEFAULT_REMOVEDFUNCTIONS_CACHEPATH, 'w').write(RemovedIndices_Text)
    print("WRITE Removed Cache:", RemovedIndices_Text)

# Main Functions


# UI Functions
def UI_SelectDatabases():
    global FUNCTIONS

    # Select Language
    USERINPUT_Language = st.selectbox("Select Language", list(DATABASES.keys()))

    # Select Databases
    Databases = DATABASES[USERINPUT_Language]
    DatabaseNames = []
    DatabasePaths = []
    for d in Databases:
        DatabaseNames.append(d['name'])
        DatabasePaths.append(d['path'])
    USERINPUT_DATABASENAMES = st.multiselect("Select Databases", DatabaseNames, default=DatabaseNames)

    USERINPUT_DATABASES = []
    for dn in USERINPUT_DATABASENAMES:
        USERINPUT_DATABASES.append(DatabasePaths[DatabaseNames.index(dn)])
    
    # Load Functions
    for d in USERINPUT_DATABASES:
        DB_functions = json.load(open(d, 'r'))["Functions"]
        FUNCTIONS[USERINPUT_Language].extend(DB_functions)
    
    # Display Database Functions Details
    st.markdown("### Found <span style=\"color:yellow\">**" + str(len(FUNCTIONS[USERINPUT_Language])) + "**</span> functions!", unsafe_allow_html=True)

    return USERINPUT_Language

def UI_DisplayFunctionDetails(f, Language='Python'):
    st.markdown("### Function Details")

    col1, col2 = st.beta_columns([1, 5])
    col1.markdown("Name")
    col2.markdown("```\n" + f['Name'])

    col1, col2 = st.beta_columns([1, 5])
    col1.markdown("Description")
    Description = ['No Description'] if len(f['Description']) == 0 else f['Description']
    col2.markdown("```\n" + '\n'.join(Description))

    col1, col2 = st.beta_columns([1, 5])
    col1.markdown("Parameters")
    col2.markdown("```" + Language.lower() + "\n" + "(" + f['Parameters'] + ")")
    
    col1, col2 = st.beta_columns([1, 5])
    col1.markdown("Imports")
    Imports = ['No Imports'] if len(f['Imports']) == 0 else f['Imports']
    col2.markdown("```" + Language.lower() + "\n" + '\n'.join(Imports))

    col1, col2 = st.beta_columns([1, 5])
    col1.markdown("Code")
    col2.markdown("```" + Language.lower() + "\n" + '\n'.join(f['Code']))

def UI_SelectFunction(functions, name="Added", CodeWindow=st, FuncCount=st, FuncSelect=st, Language='Python'):
    DisplayNames = GetFunctionDisplayNames(functions)
    FuncCount.markdown("**" + str(len(DisplayNames)) + "** " + name + " Functions")
    FunctionChoice = FuncSelect.selectbox(name + " Functions", ["Select Function"] + DisplayNames)
    FunctionChoiceIndex = -1
    if not FunctionChoice == 'Select Function':
        FunctionChoiceIndex = DisplayNames.index(FunctionChoice)
        CodeWindow.markdown("```" + Language.lower() + "\n" + '\n'.join(functions[FunctionChoiceIndex]['Code']))
    else:
        CodeWindow.markdown("")
    return FunctionChoiceIndex


# Repo Based Functions
def search_functions():
    global FUNCTIONS_HASHMAP

    # Title
    st.header("Search Functions")

    # Load Inputs
    st.markdown("## Select Database")
    USERINPUT_Language = UI_SelectDatabases()

    st.markdown("## Search")
    USERINPUT_SearchQuery = st.text_input("Enter Search Query", "BubbleSort")

    searchOptions = {'Name': True, 'Parameters': False, 'Imports': False, 'Description': False, 'Code': False}
    col1, col2, col3, col4 = st.beta_columns(4)
    searchOptions['Description'] = col1.checkbox("Search Descriptions?")
    searchOptions['Imports'] = col2.checkbox("Search Imports?")
    searchOptions['Parameters'] = col3.checkbox("Search Parameters?")
    searchOptions['Code'] = col4.checkbox("Search Code?")

    # Process Inputs
    FUNCTIONS_HASHMAP = GigaCode.GenerateFunctionHashMap(FUNCTIONS[USERINPUT_Language])
    directMatchFunctions, matchFunctions = GigaCode.SearchFunctions(FUNCTIONS_HASHMAP, USERINPUT_SearchQuery, searchOptions)

    # Display Output
    # Exact Matches
    st.markdown("## Exact Matches")
    st.markdown("### Found <span style=\"color:yellow\">**" + str(len(directMatchFunctions)) + "**</span> exact matches!", unsafe_allow_html=True)
    directMatchFunctions_DisplayNames = GetFunctionDisplayNames(directMatchFunctions)
    USERINPUT_ExactMatchChoice = st.selectbox("Exact Match Functions", ["Select Function"] + directMatchFunctions_DisplayNames)
    if not USERINPUT_ExactMatchChoice == 'Select Function':
        USERINPUT_ExactMatchChoiceIndex = directMatchFunctions_DisplayNames.index(USERINPUT_ExactMatchChoice)
        UI_DisplayFunctionDetails(directMatchFunctions[USERINPUT_ExactMatchChoiceIndex], Language=USERINPUT_Language)

    # Substring Matches
    st.markdown("## Related Matches")
    matchFunctionsCount = 0
    for k in matchFunctions.keys():
        matchFunctionsCount += len(matchFunctions[k])
    st.markdown("### Found <span style=\"color:yellow\">**" + str(matchFunctionsCount) + "**</span> related matches!", unsafe_allow_html=True)
    matchFunctions_List = matchFunctions['Name'] + matchFunctions['Description'] + matchFunctions['Imports'] + matchFunctions['Parameters'] + matchFunctions['Code']
    matchFunctions_DisplayNames = GetFunctionDisplayNames(matchFunctions_List)
    USERINPUT_RelatedMatchChoice = st.selectbox("Related Match Functions", ["Select Function"] + matchFunctions_DisplayNames)
    if not USERINPUT_RelatedMatchChoice == 'Select Function':
        USERINPUT_RelatedMatchChoiceIndex = matchFunctions_DisplayNames.index(USERINPUT_RelatedMatchChoice)
        UI_DisplayFunctionDetails(matchFunctions_List[USERINPUT_RelatedMatchChoiceIndex], Language=USERINPUT_Language)

def function_database():
    global FUNCTIONS

    # Title
    st.header("Function Database")

    # Load Inputs
    st.markdown("## Select Database")
    USERINPUT_Language = UI_SelectDatabases()

    # Functions
    st.markdown("## View Functions")
    st.markdown("### Found <span style=\"color:yellow\">**" + str(len(FUNCTIONS[USERINPUT_Language])) + "**</span> functions!", unsafe_allow_html=True)
    Functions_DisplayNames = GetFunctionDisplayNames(FUNCTIONS[USERINPUT_Language])
    USERINPUT_FunctionChoice = st.selectbox("Exact Match Functions", ["Select Function"] + Functions_DisplayNames)
    if not USERINPUT_FunctionChoice == 'Select Function':
        USERINPUT_FunctionChoiceIndex = Functions_DisplayNames.index(USERINPUT_FunctionChoice)
        UI_DisplayFunctionDetails(FUNCTIONS[USERINPUT_Language][USERINPUT_FunctionChoiceIndex], Language=USERINPUT_Language)

    # Add or Remove Existing Functions
    # Retreive Removed Cache Functions
    AddedFunctions, RemovedFunctions, AddedIndices, RemovedIndices = GetRemovedFunctions(FUNCTIONS[USERINPUT_Language])
    st.markdown("## Add/Remove Functions")
    AddedFunctions_DisplayNames = GetFunctionDisplayNames(AddedFunctions)
    RemovedFunctions_DisplayNames = GetFunctionDisplayNames(RemovedFunctions)
    USERINPUT_AddedFunctionChoiceIndex = -1
    USERINPUT_RemovedFunctionChoiceIndex = -1

    col1, col2, col3 = st.beta_columns([5, 1, 5])
    AddedFuncCount = col1.empty()
    AddedFuncSelect = col1.empty()
    AddedCode = col1.empty()
    USERINPUT_AddedFunctionChoiceIndex = UI_SelectFunction(AddedFunctions, name="Added", CodeWindow=AddedCode, FuncCount=AddedFuncCount, FuncSelect=AddedFuncSelect, Language=USERINPUT_Language)

    RemovedFuncCount = col3.empty()
    RemovedFuncSelect = col3.empty()
    RemovedCode = col3.empty()
    RemovedFuncCount.markdown("**" + str(len(RemovedFunctions_DisplayNames)) + "** Removed Functions")
    USERINPUT_RemovedFunctionChoiceIndex = UI_SelectFunction(RemovedFunctions, name="Removed", CodeWindow=RemovedCode, FuncCount=RemovedFuncCount, FuncSelect=RemovedFuncSelect, Language=USERINPUT_Language)

    col2.markdown("")
    col2.markdown("")
    USERINPUT_Remove = col2.button("->") and (USERINPUT_AddedFunctionChoiceIndex >= 0)
    USERINPUT_Add = col2.button("<-") and (USERINPUT_RemovedFunctionChoiceIndex >= 0)
    if USERINPUT_Remove:
        RemovedIndices.append(AddedIndices[USERINPUT_AddedFunctionChoiceIndex])
    if USERINPUT_Add:
        RemovedIndices.pop(USERINPUT_RemovedFunctionChoiceIndex)
    if USERINPUT_Remove or USERINPUT_Add:
        SetRemovedFunctions(RemovedIndices)
        AddedFunctions, RemovedFunctions, AddedIndices, RemovedIndices = GetRemovedFunctions(FUNCTIONS[USERINPUT_Language])
        USERINPUT_AddedFunctionChoiceIndex = UI_SelectFunction(AddedFunctions, name="Added", CodeWindow=AddedCode, FuncCount=AddedFuncCount, FuncSelect=AddedFuncSelect, Language=USERINPUT_Language)
        USERINPUT_RemovedFunctionChoiceIndex = UI_SelectFunction(RemovedFunctions, name="Removed", CodeWindow=RemovedCode, FuncCount=RemovedFuncCount, FuncSelect=RemovedFuncSelect, Language=USERINPUT_Language)

    # Download Database
    if st.button('Download Database'):
        SaveDatabaseData = {"Name": 'FunctionDatabase_' + USERINPUT_Language, "Functions": AddedFunctions}
        json.dump(SaveDatabaseData, open(DEFAULT_DATABASE_SAVEPATH, 'w'))
        link = DownloadFile(DEFAULT_DATABASE_SAVEPATH, 'FunctionDatabase_' + USERINPUT_Language + '.json', 'FunctionDatabase_' + USERINPUT_Language + '.json')
        st.markdown(link, unsafe_allow_html=True)

def parse_code():
    global FUNCTIONS

    # Title
    st.header("Parse Code")

    # Load Inputs
    # Select Language
    st.markdown("## Select Language")
    USERINPUT_Language = st.selectbox("Select Language", list(DATABASES.keys()))
    # Select Parser
    st.markdown("## Select Parser")
    Parsers = PARSER_FORMATS[USERINPUT_Language]
    ParserNames = list(Parsers.keys())
    USERINPUT_ParserName = st.selectbox("Select Parser", ["Select Parser"] + ParserNames)
    if USERINPUT_ParserName == "Select Parser":
        return
    Parser = Parsers[USERINPUT_ParserName]
    ParserFormatExample = "\n".join(json.load(open(Parser, 'r'))["Format_Example"])
    st.markdown("### Format Example")
    st.markdown('```' + USERINPUT_Language.lower() + '\n' + ParserFormatExample)

    # Get Code
    st.markdown("## Enter Code to Parse")
    USERINPUT_Code = st.text_area("Code", ParserFormatExample)

    # Process Inputs
    # Parse Code
    ParsedFunctions = []
    if not (USERINPUT_Code.strip() == ""):
        ParsedFunctions = GigaCode.ExtractPythonFunctions(data=USERINPUT_Code, formatJSONPath=Parser)
    
    # Display Outputs
    st.markdown("## View Parsed Functions")
    st.markdown("### Found <span style=\"color:yellow\">**" + str(len(ParsedFunctions)) + "**</span> functions!", unsafe_allow_html=True)
    Functions_DisplayNames = GetFunctionDisplayNames(ParsedFunctions)
    USERINPUT_FunctionChoice = st.selectbox("Exact Match Functions", ["Select Function"] + Functions_DisplayNames)
    if USERINPUT_FunctionChoice == 'Select Function': return
    USERINPUT_FunctionChoiceIndex = Functions_DisplayNames.index(USERINPUT_FunctionChoice)
    UI_DisplayFunctionDetails(ParsedFunctions[USERINPUT_FunctionChoiceIndex], Language=USERINPUT_Language)

    # Download Database
    if st.button('Download Parsed Database'):
        SaveDatabaseData = {"Name": 'FunctionDatabase_' + USERINPUT_Language, "Functions": ParsedFunctions}
        json.dump(SaveDatabaseData, open(DEFAULT_DATABASE_SAVEPATH, 'w'))
        link = DownloadFile(DEFAULT_DATABASE_SAVEPATH, 'FunctionDatabase_' + USERINPUT_Language + '.json', 'FunctionDatabase_' + USERINPUT_Language + '.json')
        st.markdown(link, unsafe_allow_html=True)

#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()