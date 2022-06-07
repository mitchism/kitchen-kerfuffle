# Recipe class
class Recipe:
    def __init__(self,title,ingredients,instructions,url,recipe_id,recipe_num):
        
        self.title = title.title() #.title() method to standardize use of caps        
        self.link = url
        self.steps = instructions
        
        # to facilitate possible SQL integrations, these fields can serve as keys
        self.id_pfkey = recipe_id #foreign primary key
        self.id_skey = recipe_num #surrogate key - running tally
        
        # ALL ingredients 
        self.ingredients = set()
        for item in ingredients:
            self.ingredients.add(item)
        self.ingreds_count_total = len(self.ingredients)

        # MATCHING ingredients
        self.ingredients_matching = set()
        self.ingreds_count_matching = len(self.ingredients_matching)

        # MISSING ingredients
        self.ingredients_missing = set()
        self.ingreds_count_missing = len(self.ingredients_missing)

        # FRACTION - ingredients matching of total
        if self.ingreds_count_total > 0:
            fraction = (self.ingreds_count_matching / self.ingreds_count_total)
        else:
            fraction = ''
        self.fraction_user_ingreds = round(fraction,2)
        
    def update_counts(self):
        self.ingreds_count_total = len(self.ingredients)
        self.ingreds_count_matching = len(self.ingredients_matching)
        self.ingreds_count_missing = len(self.ingredients_missing)
        
        #fraction = (self.ingreds_count_matching / self.ingreds_count_total)
        if self.ingreds_count_total > 0:
            fraction = (self.ingreds_count_matching / self.ingreds_count_total)
        else:
            fraction = ''
        self.fraction_user_ingreds = round(fraction,2)

    def __str__(self):
        self.update_counts()
        '''
        ingred_statement = ''
        steps_statement = ''
        for x in self.ingredients:
            ingred_statement += '{}; '.format(x)
        for x in self.steps:
            steps_statement += '{}; '.format(x)
        '''
        #print(
        return f" >> Recipe Title: \t''{self.title}'' \n \
            \t\tlink: \t {self.link} \n\
            \t\tIngredients Available: \t{self.ingreds_count_matching} out of {self.ingreds_count_total}\n \
            \t\tIngredients required: {self.ingredients}\
            \t\tInstructions: {self.steps}" #\
            #\t\tIngredients Required: \t{self.ingredients}\n \
            #\t\tInstructions: \t{self.steps} \
            #")

class User():
    def __init__(self,name):
        self.name = name
        
        self.ingredients = []
        self.restrictions = []
        self.regex_statement = ''
        self.results = []
        self.result_number = 0
    
    def __str__(self):
        return f'User {self.name} has {len(self.ingredients)} ingredients available'

    def regex_for_search(self):
        keyw_i = 0
        for item in self.ingredients:
            if keyw_i+1 == 1:
                keyw = '('+item+'|'
                keyw_i += 1
            elif keyw_i+1 > 1 and keyw_i+1 < len(self.ingredients):
                keyw += item+'|'
                keyw_i += 1
            elif keyw_i+1 >= len(self.ingredients):
                keyw += item+')'

        regex_prefix = '(^|\s{1})'
        regex_statement = f"{regex_prefix}{keyw}"
        self.regex_statement = regex_statement
        return regex_statement

    def reset(self):
        self.ingredients = []
        self.restrictions = []
        self.regex_statement = ''
        self.results = []
        self.result_number = 0
    
    def add_ingredient(self,ingredient):
        self.ingredients.append(ingredient)
        self.regex_statement = self.regex_for_search()

    def add_ingredients(self,ingredientlist):
        self.ingredients.extend(ingredientlist)
        self.regex_statement = self.regex_for_search()
        
    def add_restriction(self,ingredient):
        self.restrictions.append(ingredient)

    def add_search_result(self,recipe):
        import re

        for ingred_i in recipe.ingredients:
            match = re.findall(f"({self.regex_statement})", ingred_i)
            if match != []:
                recipe.ingredients_matching.add(ingred_i)
            else:
                recipe.ingredients_missing.add(ingred_i)
        
        recipe.update_counts()
        self.result_number += 1
        result_entry =  (self.result_number, recipe, recipe.ingreds_count_total, recipe.fraction_user_ingreds, recipe.ingreds_count_missing)

        self.results.append(result_entry)

    def sort_search_results(self):
        temp = sorted(self.results,key=lambda x: 1/x[3])
        self.results = sorted(temp,key=lambda x: x[4])

    def show_search_results(self):
        for result in self.results:
            print(result[1])
            #print(f"result no.: {result[0]}, recipe title: {result[1].title}, # ingreds: {result[2]}, #fraction matched = {result[3]}\n")

    def export_results_as_df(self):
        import pandas as pd
        #results_list = user.results[:]

        output_dict = {}
        output_dict['title'] = []
        #output_dict['%ingred. on hand'] = []
        #output_dict['all ingredients'] = []
        output_dict['number ingreds.'] = []
        
        output_dict['matched ingredients'] = []
        output_dict['missing ingredients'] = [] 

        output_dict['instructions'] = []
        output_dict['url'] = []

        #for result in results_list:
        for result in self.results:
            if result[1].ingreds_count_total > 1:
                output_dict['title'].append(result[1].title)
                #output_dict['%ingred. on hand'].append(result[1].title)
                #output_dict['all ingredients'].append(result[1].ingredients)
                
                num_own = result[1].ingreds_count_matching
                num_total = result[1].ingreds_count_total

                output_dict['number ingreds.'].append(f"{num_own} of {num_total}")

                ingred_match_txt = ''
                ingred_miss_txt = ''
                i = 1
                for x in result[1].ingredients_matching:
                    #ingred_match_txt += '{}; '.format(x)
                    #x2 = x.replace(" (","<br>(")
                    x2 = x.replace(" (","  (")
                    ingred_match_txt += f'<b>{i}.</b>  {x2}<br>'
                    i += 1

                #j = 1
                for x in result[1].ingredients_missing:
                    #ingred_miss_txt += '{}; '.format(x)
                    #ingred_miss_txt += f'{j}. {x}<br>'
                    #j += 1
                    #x2 = x.replace(" (","<br>   (")
                    x2 = x.replace(" (","  (")
                    ingred_miss_txt += f'<b>{i}.</b>  {x2}<br>'
                    i += 1

                #output_dict['matched ingredients'] += ingred_match_txt
                #output_dict['missing ingredients'] += ingred_miss_txt
                output_dict['matched ingredients'].append(ingred_match_txt)
                output_dict['missing ingredients'].append(ingred_miss_txt)
                
                recipe_steps = result[1].steps
                output_dict['instructions'].append(recipe_steps.replace("..Step","..<br>Step"))

                output_dict['url'].append(f"<a href={result[1].link}>Link</a>")
            else:
                pass

        #outputdf = pd.DataFrame(data=output_dict)
        df = pd.DataFrame(data=output_dict)
        #df.head()
        if len(df)<100:
            return df
        else:
            return df.iloc[:100, :]
'''
class User():
    def __init__(self,name):
        self.name = name # could use name.lower() to avoid capitalization inconsistencies in their names
        
        self.ingredients = []
        self.restrictions = []
        self.search_results = []
        self.num_results = len(self.search_results)
    
    def __str__(self):
        return f'User {self.name} has {len(self.ingredients)} ingredients available'
    
    def reset(self):
        self.ingredients = []
        self.restrictions = []
        self.recipes_search_list = []
    
    def add_ingredient(self,ingredient):
        self.ingredients.append(ingredient)
        
    def add_restriction(self,ingredient):
        self.ingredients.append(ingredient)
    

class SearchResult(Recipe):
    def __init__(self):
        Recipe.__init__(self)
        # store ingredient search results
        self.ingredients_matching = set()
        self.ingredients_count_matching = 0 
        
        self.ingredients_fraction = (self.ingredients_count_matching / self.ingredients_count_total)

    def add_search_result(self,recipex):
        
        result_num = self.num_results+1
        
        result_entry =  (result_num, recipex.ingredients_fraction, recipex)

        self.search_results.append(result_entry)

    def add_ingred_match(self,ingred):
        self.ingredients_matching.add(ingred)
        self.ingredients_count_matching = len(self.ingredients_matching)
        self.ingredients_fraction = (self.ingredients_count_matching / self.ingredients_count_total)
        

class SearchResults():
    def __init__(self):
        self.results = []
        self.num_results = 0


    def add_search_result(self,recipe):
        
        result_num = self.num_results+1
        
        result_entry =  (self.result_num, recipe, recipe.ingredients_fraction)

        self.search_results.append(result_entry)

    def add_ingred_match(self,ingred):
        self.ingredients_matching.add(ingred)
        self.ingredients_count_matching = len(self.ingredients_matching)
        self.ingredients_fraction = (self.ingredients_count_matching / self.ingredients_count_total)
        
'''

    