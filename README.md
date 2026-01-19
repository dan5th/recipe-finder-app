# Recipe Finder 🍳

A Streamlit app that helps you find recipes based on ingredients you have on hand.

## Features

- **Ingredient Search**: Enter one or more ingredients to find matching recipes
- **Smart Matching**: Fuzzy matching handles variations (e.g., "chicken" matches "chicken breasts")
- **AND Logic**: Shows only recipes containing ALL your specified ingredients
- **PDF Preview**: View recipe PDFs directly in the app
- **Quick Add**: Common ingredients available as one-click buttons

## Live Demo

[View on Streamlit Community Cloud](https://your-app-url.streamlit.app)

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

## Project Structure

```
recipe-finder-app/
├── recipe_finder_app.py    # Main Streamlit application
├── recipes_data.json       # Recipe database with ingredients
├── requirements.txt        # Python dependencies
├── README.md
└── pdfs/                   # Recipe PDF files
    ├── recipe-name-1.pdf
    ├── recipe-name-2.pdf
    └── ...
```

## Usage

1. Add ingredients using the sidebar:
   - Type an ingredient and click "Add"
   - Or click quick-add buttons for common ingredients

2. View matching recipes in the main area

3. Click "View Recipe" to see the full PDF

4. Click "Back to Results" to return to search

## Adding Your Own Recipes

1. Place PDF files in the `pdfs/` folder

2. Add entries to `recipes_data.json`:
   ```json
   {
     "name": "Recipe Name",
     "filename": "recipe-file.pdf",
     "ingredients_raw": ["1 cup flour", "2 eggs"],
     "ingredients_normalized": ["flour", "eggs"],
     "ingredient_count": 2
   }
   ```

## Deployment to Streamlit Community Cloud

1. Push your code to GitHub (including the `pdfs/` folder)

2. Go to [share.streamlit.io](https://share.streamlit.io)

3. Connect your GitHub repo

4. Deploy!

**Note:** Large PDF collections will increase your repo size. Consider using [Git LFS](https://git-lfs.github.com/) for better handling of large files.

## License

MIT License
