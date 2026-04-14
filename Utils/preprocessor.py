import pandas as pd
import ast

NON_VEG_KEYWORDS = [
    'chicken', 'beef', 'pork', 'fish', 'salmon', 'tuna', 'shrimp', 'prawn',
    'bacon', 'sausage', 'ham', 'turkey', 'duck', 'lamb', 'mutton', 'meat',
    'gelatin', 'anchovy', 'clam', 'oyster', 'lobster', 'crab'
]

def is_vegetarian(ingredients):
    """Simple check to filter vegetarian recipes."""
    if isinstance(ingredients, str):
        try:
            ing_list = ast.literal_eval(ingredients)
        except:
            ing_list = ingredients.split(',')
    else:
        ing_list = ingredients
    
    ing_text = ' '.join(str(item).lower() for item in ing_list)
    for keyword in NON_VEG_KEYWORDS:
        if keyword in ing_text:
            return False
    return True


def clean_ingredients(ingredients):
    """Clean ingredients list into a single string."""
    if isinstance(ingredients, str):
        try:
            ing_list = ast.literal_eval(ingredients)
        except:
            ing_list = ingredients.split(',')
    else:
        ing_list = ingredients
    
    cleaned = []
    for item in ing_list:
        item = str(item).lower().strip()
        # Remove common quantity patterns
        words = item.split()
        cleaned_words = [w for w in words if not (w[0].isdigit() and len(w) <= 4)]
        cleaned.append(' '.join(cleaned_words))
    return ' '.join(cleaned)


def load_and_filter_vegetarian_recipes(raw_path='RAW_recipes.csv', 
                                      output_path='data/vegetarian_recipes.csv'):
    """Load raw dataset, filter vegetarian recipes, and save."""
    print("Loading raw recipes file...")
    df = pd.read_csv(raw_path)
    
    print("Filtering only vegetarian recipes...")
    df['is_veg'] = df['ingredients'].apply(is_vegetarian)
    df_veg = df[df['is_veg']].copy()
    
    print(f"✅ Found {len(df_veg)} vegetarian recipes out of {len(df)} total.")
    
    df_veg['ingredients_str'] = df_veg['ingredients'].apply(clean_ingredients)
    
    # Keep important columns
    columns_to_keep = ['name', 'ingredients', 'ingredients_str', 'steps', 'minutes', 'nutrition', 'tags']
    df_veg = df_veg[columns_to_keep]
    
    df_veg.to_csv(output_path, index=False)
    print(f"✅ Vegetarian recipes saved to {output_path}")
    return df_veg