import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VegetarianRecommender:
    def __init__(self, data_path='data/vegetarian_recipes.csv'):
        self.df = pd.read_csv(data_path)
        self.tfidf = None
        self.tfidf_matrix = None
        self._build_model()
    
    def _build_model(self):
        """Build TF-IDF model."""
        self.tfidf = TfidfVectorizer(
            stop_words='english', 
            min_df=2, 
            max_features=5000
        )
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['ingredients_str'])
        print(f"✅ Model built with {len(self.df)} vegetarian recipes.")
    
    def recommend(self, user_ingredients: list, top_n: int = 5):
        """Recommend top matching vegetarian recipes."""
        user_str = ' '.join([ing.lower().strip() for ing in user_ingredients])
        user_vec = self.tfidf.transform([user_str])
        
        sim_scores = cosine_similarity(user_vec, self.tfidf_matrix).flatten()
        
        top_indices = sim_scores.argsort()[-top_n:][::-1]
        
        recommendations = self.df.iloc[top_indices][['name', 'ingredients', 'steps', 'minutes']].copy()
        recommendations['similarity_score'] = sim_scores[top_indices].round(3)
        
        return recommendations.reset_index(drop=True)