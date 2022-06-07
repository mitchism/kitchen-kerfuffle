from functions_pandasdata_io import jsonread_compressed
from functions import initialize_testconfig, search_query, test_func, user_input
from classes import Recipe, User

from jinja2 import Environment, FileSystemLoader

name = '../recipedata/recipesdf'
pref = 'table'

df = jsonread_compressed(name,pref)

# Instantiate User object
user = user_input('username')
#user = initialize_testconfig()

# execute search
search_query(user,df)

# export user search results
df = user.export_results_as_df()

# df to html 
htmldf = df.to_html(escape=False)


# render content into jinja2 template 
env = Environment(loader=FileSystemLoader('.'))

template = env.get_template('../templates/template_for_report.html')
template_vars = {"title" : "Recipes Search Results","table": htmldf}

renderedhtml = template.render(template_vars)
with open("../search_results_output.html","w") as f:
    f.write(renderedhtml)