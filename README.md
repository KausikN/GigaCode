# GigaCode
 GigaCode is a functions and code parsing tool for various languages

 Hosted at [https://infinityjoker-codeparsers.herokuapp.com/](https://infinityjoker-codeparsers.herokuapp.com/)

# GUI
 - Install streamlit using
   ```
   pip install streamlit
   ```
 - Launch Streamlit GUI in the repo folder by
   ```
   streamlit run app.py
   ```

# Parse Functions
   
   - Implemented for Python functions
   
     Parses code written in a format specified below

     ![Python Format](DocImages/FunctionStandardFormat_1.png)
    
     Gets the function name, parameters, description, imports and code from the parsed data.

# Function Database

   - Store parsed function data in pickle/json files as database of functions for later use

   - (OR) Run app_Database.py for storing new functions in a database pickle/json file

   ![Database App](DocImages/DatabaseApp_1.PNG)

# Search Functions

   - Search for functions by input query from database pickle/json files

   - (OR Run app_FunctionsView.py for searching functions

   ![Search App](DocImages/SearchApp_1.PNG)