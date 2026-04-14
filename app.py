import streamlit as st
import pandas as pd
from recommender.model import VegetarianRecommender
from Utils.preprocessor import load_and_filter_vegetarian_recipes

import sys
print(sys.path)


st.set_page_config(page_title="🥗 Veg Recipe Recommender", layout="wide")
st.title("🥗 Vegetarian Recipe Recommender")
st.markdown("Enter ingredients you have at home and get delicious **vegetarian** recipe suggestions!")

# Sidebar
st.sidebar.header("Settings")
top_n = st.sidebar.slider("Number of recommendations", 3, 10, 5)
max_time = st.sidebar.slider("Max cooking time (minutes)", 10, 120, 60)

# Check if vegetarian data exists
data_path = "data/vegetarian_recipes.csv"

if not pd.io.common.file_exists(data_path):
    st.warning("Vegetarian dataset not found. Creating it now... (This may take 1-2 minutes)")
    if st.button("Start Filtering Vegetarian Recipes"):
        with st.spinner("Filtering recipes..."):
            load_and_filter_vegetarian_recipes()
        st.success("Dataset ready!")
        st.rerun()
else:
    st.success("Vegetarian dataset loaded successfully!")

# Initialize recommender
if pd.io.common.file_exists(data_path):
    if 'recommender' not in st.session_state:
        with st.spinner("Loading recommendation model..."):
            st.session_state.recommender = VegetarianRecommender(data_path)
    
    # User input
    user_input = st.text_area(
        "Enter ingredients you have (comma separated)",
        placeholder="paneer, tomato, onion, garlic, spinach, rice, cumin",
        height=100
    )

    if st.button("🔍 Get Vegetarian Recipes", type="primary"):
        if user_input.strip():
            ingredients = [ing.strip() for ing in user_input.split(',') if ing.strip()]
            
            with st.spinner("Finding best matches..."):
                recs = st.session_state.recommender.recommend(ingredients, top_n=top_n)
                
                # Apply time filter
                recs = recs[recs['minutes'] <= max_time]
            
            if len(recs) == 0:
                st.warning("No recipes found within your time limit. Try increasing max time.")
            else:
                st.subheader(f"Here are your top {len(recs)} vegetarian recommendations:")
                
                for i, row in recs.iterrows():
                    with st.expander(f"🍛 **{row['name']}**  —  ⏱️ {row['minutes']} mins  —  Score: {row['similarity_score']}"):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.write("**Ingredients:**")
                            st.write(row['ingredients'])
                        with col2:
                            st.write("**Steps:**")
                            steps_text = row['steps']
                            if isinstance(steps_text, str) and steps_text.startswith('['):
                                try:
                                    steps_list = eval(steps_text)
                                    for idx, step in enumerate(steps_list, 1):
                                        st.write(f"{idx}. {step}")
                                except:
                                    st.write(steps_text)
                            else:
                                st.write(steps_text)
        else:
            st.warning("Please enter at least one ingredient.")

# Footer
st.caption("Built with TF-IDF + Cosine Similarity | Only Vegetarian Recipes")