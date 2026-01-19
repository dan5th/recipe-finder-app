# Recipe Finder 🍳

A Streamlit app that helps you find recipes based on ingredients you have on hand.

## Features

- **Ingredient Search**: Enter one or more ingredients to find matching recipes
- **Smart Matching**: Fuzzy matching handles variations (e.g., "chicken" matches "chicken breasts")
- **AND Logic**: Shows only recipes containing ALL your specified ingredients
- **PDF Preview**: View recipe PDFs directly in the app
- **Quick Add**: Common ingredients available as one-click buttons

## Screenshot

![Recipe Finder App](screenshot.png)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/recipe-finder-app.git
   cd recipe-finder-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run recipe_finder_app.py
   ```

4. Open your browser to `http://localhost:8501`

## Usage

1. Add ingredients using the sidebar:
   - Type an ingredient and click "Add"
   - Or click quick-add buttons for common ingredients

2. View matching recipes in the main area

3. Click "View Recipe" to see the full PDF

4. Click "Back to Results" to return to search

## Files

- `recipe_finder_app.py` - Main Streamlit application
- `recipes_data.json` - Recipe database with ingredients
- `requirements.txt` - Python dependencies

## Adding Your Own Recipes

The `recipes_data.json` file contains recipe data in this format:

```json
{
  "name": "Recipe Name",
  "filename": "recipe-file.pdf",
  "ingredients_raw": ["1 cup flour", "2 eggs"],
  "ingredients_normalized": ["flour", "eggs"],
  "ingredient_count": 2
}
```

To add recipes:
1. Place PDF files in the same directory as the app
2. Add entries to `recipes_data.json` with normalized ingredient names

## License

MIT License
