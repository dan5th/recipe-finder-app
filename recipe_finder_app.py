"""
Recipe Finder - Streamlit App
Search for recipes by ingredients and view PDFs!

To run: streamlit run recipe_finder_app.py
"""

import streamlit as st
import json
import re
import base64
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Recipe Finder",
    page_icon="🍳",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .ingredient-have {
        background: #d4edda;
        color: #155724;
        padding: 2px 8px;
        border-radius: 12px;
        margin: 2px;
        display: inline-block;
        font-size: 0.85rem;
    }
    .ingredient-other {
        background: #f0f0f0;
        color: #666;
        padding: 2px 8px;
        border-radius: 12px;
        margin: 2px;
        display: inline-block;
        font-size: 0.85rem;
    }
    .recipe-card {
        padding: 1rem;
        border: 2px solid #f0f0f0;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        cursor: pointer;
    }
    .recipe-card:hover {
        border-color: #667eea;
        background: #fafafa;
    }
    .stats-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_recipes():
    """Load recipe data from JSON file."""
    json_path = Path(__file__).parent / "recipes_data.json"

    if not json_path.exists():
        st.error(f"Recipe data not found at {json_path}")
        return []

    with open(json_path, 'r') as f:
        return json.load(f)


def normalize_text(text):
    """Normalize text for matching."""
    if not text:
        return ''
    return re.sub(r'[^a-z ]', '', text.lower()).strip()


def ingredient_matches(user_ing, recipe_ing):
    """Check if user ingredient matches a recipe ingredient."""
    user = normalize_text(user_ing)
    recipe = normalize_text(recipe_ing)

    if not user or not recipe:
        return False

    # Direct contains match
    if user in recipe or recipe in user:
        return True

    # Word-level match
    user_words = [w for w in user.split() if len(w) >= 3]
    recipe_words = [w for w in recipe.split() if len(w) >= 2]

    for uw in user_words:
        for rw in recipe_words:
            if uw in rw or rw in uw:
                return True

    return False


def find_matching_recipes(recipes, user_ingredients):
    """Find recipes containing ALL user ingredients."""
    if not user_ingredients:
        return []

    results = []

    for recipe in recipes:
        normalized = recipe.get('ingredients_normalized', [])
        if not normalized:
            continue

        # Check if recipe has ALL user ingredients
        matched = []
        has_all = True

        for user_ing in user_ingredients:
            found = False
            for recipe_ing in normalized:
                if ingredient_matches(user_ing, recipe_ing):
                    found = True
                    matched.append(recipe_ing)
                    break

            if not found:
                has_all = False
                break

        if has_all:
            other = [ing for ing in normalized if ing not in matched]
            results.append({
                'name': recipe['name'],
                'filename': recipe['filename'],
                'matched': matched,
                'other': other,
                'total': len(normalized)
            })

    # Sort alphabetically
    results.sort(key=lambda x: x['name'])
    return results


def display_pdf(pdf_path):
    """Display PDF in Streamlit."""
    try:
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        pdf_display = f'''
            <iframe
                src="data:application/pdf;base64,{base64_pdf}"
                width="100%"
                height="800"
                type="application/pdf"
                style="border: none; border-radius: 8px;">
            </iframe>
        '''
        st.markdown(pdf_display, unsafe_allow_html=True)
        return True
    except Exception as e:
        st.error(f"Error loading PDF: {e}")
        return False


def main():
    # Header
    st.markdown('<h1 class="main-header">🍳 Recipe Finder</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Search for recipes by ingredients</p>', unsafe_allow_html=True)

    # Load recipes
    recipes = load_recipes()

    if not recipes:
        st.error("No recipes loaded. Please ensure recipes_data.json is in the same directory.")
        return

    # Initialize session state
    if 'ingredients' not in st.session_state:
        st.session_state.ingredients = []
    if 'selected_recipe' not in st.session_state:
        st.session_state.selected_recipe = None

    # Sidebar
    with st.sidebar:
        st.header("🥕 Your Ingredients")

        # Input for new ingredient
        new_ingredient = st.text_input(
            "Add an ingredient",
            placeholder="e.g., chicken, cheese...",
            key="new_ingredient_input"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Add", use_container_width=True):
                if new_ingredient and new_ingredient.lower() not in [i.lower() for i in st.session_state.ingredients]:
                    st.session_state.ingredients.append(new_ingredient.lower())
                    st.session_state.selected_recipe = None
                    st.rerun()

        with col2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.ingredients = []
                st.session_state.selected_recipe = None
                st.rerun()

        # Quick add buttons
        st.markdown("**Quick Add:**")
        common = ["chicken", "beef", "salmon", "pork", "rice", "pasta", "potato", "cheese", "garlic", "onion", "tomato", "eggs"]

        cols = st.columns(3)
        for i, ing in enumerate(common):
            with cols[i % 3]:
                if st.button(ing, key=f"quick_{ing}", use_container_width=True):
                    if ing not in st.session_state.ingredients:
                        st.session_state.ingredients.append(ing)
                        st.session_state.selected_recipe = None
                        st.rerun()

        st.divider()

        # Show current ingredients
        if st.session_state.ingredients:
            st.markdown("**Your ingredients:**")
            for ing in st.session_state.ingredients:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"• {ing}")
                with col_b:
                    if st.button("✕", key=f"del_{ing}"):
                        st.session_state.ingredients.remove(ing)
                        st.session_state.selected_recipe = None
                        st.rerun()
        else:
            st.info("Add ingredients to search!")

        st.divider()

        # Stats
        st.markdown(f"""
        <div class="stats-box">
            <h4>📊 Database</h4>
            <p><strong>{len(recipes)}</strong> recipes</p>
        </div>
        """, unsafe_allow_html=True)

    # Main content area
    if st.session_state.selected_recipe:
        # Show PDF preview
        recipe = st.session_state.selected_recipe

        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"📖 {recipe['name']}")
        with col2:
            if st.button("← Back to Results", use_container_width=True):
                st.session_state.selected_recipe = None
                st.rerun()

        # Display PDF
        pdf_path = Path(__file__).parent / recipe['filename']
        if pdf_path.exists():
            display_pdf(pdf_path)
        else:
            st.error(f"PDF file not found: {recipe['filename']}")

    else:
        # Show search results
        st.subheader("📖 Matching Recipes")

        if not st.session_state.ingredients:
            st.info("👈 Add ingredients in the sidebar to search for recipes!")
        else:
            matches = find_matching_recipes(recipes, st.session_state.ingredients)

            if not matches:
                search_terms = ", ".join(st.session_state.ingredients)
                st.warning(f"No recipes found containing all of: **{search_terms}**\n\nTry removing some ingredients.")
            else:
                st.success(f"Found **{len(matches)}** recipe{'s' if len(matches) != 1 else ''} with all your ingredients!")

                for i, recipe in enumerate(matches):
                    with st.container():
                        col1, col2 = st.columns([4, 1])

                        with col1:
                            st.markdown(f"**{recipe['name']}**")

                            # Show ingredients
                            ing_html = ""
                            for ing in recipe['matched']:
                                ing_html += f'<span class="ingredient-have">✓ {ing}</span> '
                            for ing in recipe['other']:
                                ing_html += f'<span class="ingredient-other">{ing}</span> '

                            st.markdown(ing_html, unsafe_allow_html=True)

                        with col2:
                            if st.button("View Recipe", key=f"view_{i}", use_container_width=True):
                                st.session_state.selected_recipe = recipe
                                st.rerun()

                        st.divider()


if __name__ == "__main__":
    main()
