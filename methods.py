
import requests
from models import db, connect_db, User, Cocktail, Notes, Saved, UserCocktail

class CocktailDetails:
    def __init__(self, id, name, alcoholic, glass, img, recipe, instructions):
        self.drink_id = id
        self.instructions = instructions
        self.name = name
        self.alcoholic = alcoholic
        self.glass = glass
        self.img = img
        self.recipe = recipe



def get_random_cocktail(cocktails_url):
    """return a random cocktail"""

    r = requests.get(f"{cocktails_url}random.php")
    data = r.json()
    drink = data['drinks'][0]
    drink_id = drink['idDrink']
    name = drink['strDrink']
    instructions = drink['strInstructions']
    alcoholic = drink['strAlcoholic']
    glass = drink['strGlass']
    img = drink['strDrinkThumb']
    recipe = get_ingredients(drink)

    return CocktailDetails(drink_id, name, alcoholic, glass, img, recipe, instructions)


def get_ingredients(obj):
    """get list ingredients"""

    ingredients = []
    for i in range(1, 16):
        if not obj[f'strIngredient{i}']:
            return ingredients
        else:
            ingredients.append({"ingredient": obj[f'strIngredient{i}'],
                                    "measurement": obj[f'strMeasure{i}']
                                })
    

