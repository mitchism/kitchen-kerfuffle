import json
import re
import pandas as pd

def load_dataset(filepath):
    with open(filepath) as data_file:
        datax = json.load(data_file)
    return datax

# Dict Indexed by Ingredient
def build_dictionary(datax):
    index = {}
    ingredient_keynum = 0
    recipes = {}
    recipe_num = 0
    for i in range(len(datax)):
        recipe = datax[i]['title']
        recipe_id = datax[i]['id']
        url = datax[i]['url']
        instructions_as_string = ""
        instructions_as_list = []
        ingredients_as_string = "" # New! not tested
        ingredients_as_list = [] # New! not tested

        #if recipe_id not in recipes:
        if recipe_id not in recipes:
            recipe_num += 1
            recipes[recipe_id] = {}
            recipes[recipe_id]['title'] = recipe
            recipes[recipe_id]['recipe_num'] = recipe_num
            

        elif recipe_id in recipes:
            recipe_num += 0
        
        for k in range(len(datax[i]['instructions'])):
            step = f"Step {k+1}: {datax[i]['instructions'][k]['text']}."
            instructions_as_string += step
            instructions_as_list.append(step)
        for j in range(len(datax[i]['ingredients'])):
            ingredient = datax[i]['ingredients'][j]['text']
            qty = datax[i]['quantity'][j]['text']
            unit = datax[i]['unit'][j]['text']
            weight = f"{round(datax[i]['weight_per_ingr'][j],2)} g"
            amount = f"{qty} {unit}"
            
            infostring = f"{ingredient} ({amount} or {weight}); " # New! not tested
            
            index[ingredient_keynum] = {}
            
            index[ingredient_keynum]['recipe'] = recipe
            index[ingredient_keynum]['recipe_num'] = recipe_num
            index[ingredient_keynum]['ingredient'] = ingredient
            index[ingredient_keynum]['amount'] = amount
            index[ingredient_keynum]['weight'] = weight
            
            ingredients_as_string += infostring # New! not tested
            ingredients_as_list.append(infostring) # New! not tested

            index[ingredient_keynum]['instructions_string'] = instructions_as_string
            index[ingredient_keynum]['instructions_list'] = instructions_as_list
            index[ingredient_keynum]['url'] = url
            
            ingredient_keynum += 1

        recipes[recipe_id]['ingredients_string'] = ingredients_as_string # New! not tested
        recipes[recipe_id]['ingredients_list'] = ingredients_as_list # New! not tested
        recipes[recipe_id]['instructions_string'] = instructions_as_string
        recipes[recipe_id]['instructions_list'] = instructions_as_list
        recipes[recipe_id]['url'] = url
    return recipes

def build_recipes_df(recipes):
    df0 = pd.DataFrame.from_dict(recipes)
    recipes_df = df0.transpose()
    recipes_df.reset_index(inplace=True)
    recipes_df.rename(columns={'index':'recipe_id'},inplace=True)
    recipes_df.reset_index(drop=True,inplace=True)
    return recipes_df

def initialize_testconfig():
    from classes import User
    
    user = User('username')
    for x in ['pineapple', 'orange', 'banana', 'apple']:
        user.add_ingredient(x)
    return user

def search_query(user,df):
    from classes import Recipe
    
    #print()
    regex_statement = user.regex_for_search()

    #for i in range(250):
    for i in range(len(df)):
        #number_of_ingredients_matched = 0
        #matching_ingredients = set()
        #title = df['title'][i]

        related_ingredients = df['ingredients_string'][i]
        
        #related_ingredients_list = df['ingredients_list'][i]
        #number_of_ingredients_total = len(df['ingredients_list'][i])
        #instructions = df['instructions_string'][i]
        #url = df['url'][i]
        #recipe_id = df['recipe_id'][i]
        #recipe_num = df['recipe_num'][i]
        
        search_target_1 = related_ingredients
        #search_target_2 = related_ingredients_list
        #search1 = re.findall(f"({regex_prefix}{regex_keyw})", search_target_1)
        search1 = re.findall(f"({regex_statement})", search_target_1)
        
        if len(search1) > 0:
            matching_ingredients = set()
            title = df['title'][i]
            related_ingredients_list = df['ingredients_list'][i]
            number_of_ingredients_total = len(df['ingredients_list'][i])
            instructions = df['instructions_string'][i]
            url = df['url'][i]
            recipe_id = df['recipe_id'][i]
            recipe_num = df['recipe_num'][i]
            #print(f"Adding recipe #{user.result_number}: \t{title} (id: {recipe_id})")

            result = Recipe(title,related_ingredients_list,instructions,url,recipe_id,recipe_num)
            #result.update_counts()
            user.add_search_result(result)
    
    user.sort_search_results()
    #user.show_search_results()

def test_func(user):
    from classes import User
    #userx = User()
    return user.name
    #regex_statement = User.get_search_regex()
    #print(regex_statement)
    #print(user.name)

# New improved version
def user_input(username):
    from classes import User
    user = User(username)
    user_ingredients = []
    ingredientx = input("Please enter each ingredient:\t")
    while True:
        user_ingredients.append(ingredientx)
        #user.add_ingredient(x)
        ingredientx = input("Please enter the next ingredient, or hit return to exit.:\t")
        
        if ingredientx != '':
            continue
        elif ingredientx == '':
            print(f"\nThank you. \n\tYou have entered: {user_ingredients}\n")
            break
    
    #return user_ingredients
    user.add_ingredients(user_ingredients)
    return user