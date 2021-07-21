# GigaCode
 GigaCode is a functions and code parsing tool for various languages

# GUI
[![https://infinityjoker-apps.herokuapp.com/](https://pyheroku-badge.herokuapp.com/?app=infinityjoker-apps&style=plastic)](https://infinityjoker-apps.herokuapp.com/)

 - GUI built using streamlit
 - To use app locally,
    - Clone the repo and run [StartUI.sh](StartUI.sh) to view the app on your browser!
 - App is also hosted remotely on heroku using my common host app,
    - [https://infinityjoker-apps.herokuapp.com/](https://infinityjoker-apps.herokuapp.com/)

    - In the Common Host App, simply choose a project to load and click load and deploy.

    - Then go ahead and use the app! :)

    - If you want to change to another app, simply click on View Other Projects in top left and choose any other project and load and deploy.

# Parse Functions
   
   - Implemented for Python functions
   
     Parses code written in a format specified below

     ![Python Format](DocImages/FunctionStandardFormat_1.png)
    
     Gets the function name, parameters, description, imports and code from the parsed data.

# Function Database

   - Store parsed function data in pickle/json files as database of functions for later use

# Search Functions

   - Search for functions by input query from database pickle/json files