# kitchen-kerfuffle
In a pinch? Feed me a list of recipes, and get a great meal to cook!

### general info
The database is a JSON-structure file in `./recipedata/`. <br></br>
The object classes, function definitions, and main script are in `./kitchen_kerfuffle/`. <br></br>
The html template that search results table is populated into is `./templates/`. <br> </br>

### to use the app: 
1) download the source code.
2) In python, execute `./kitchen_kerfuffle/kitchen_kerfuffle.py`.
3) after step 2, an interactive prompt will follow. enter whichever ingredients you'd like to use.
4) following completion of step 3, jinja2 renders the search results table into an html page which will appear at: `./search_results_output.html` .
