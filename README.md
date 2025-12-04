# 🎬 IMDB Top 250 Movie Recommender

A comprehensive Streamlit web application for exploring, analyzing, and getting recommendations from IMDB's Top 250 movies.

## Features

### 🏠 Home
- Overview statistics (total movies, average rating, year range, genres)
- Top rated movies showcase
- Recent additions
- Quick insights with interactive charts

### 🔍 Find Movies
- **Advanced Filtering:**
  - Filter by multiple genres
  - Year range slider
  - Minimum rating filter
  - Search by title, director, or actor
- **Sorting Options:** Rating, Year, Title
- **Download:** Export filtered results as CSV

### 📊 Analytics
- **Trends:** Movies over time, ratings by decade, duration analysis
- **Genres:** Top genres, distribution charts, popular combinations
- **Directors:** Most prolific directors, average ratings
- **Ratings:** Distribution, statistics, rating vs year correlation

### 🎭 Compare Movies
- Side-by-side comparison of 2-3 movies
- Visual charts comparing ratings and release years
- Detailed information display

### ⭐ Top Lists
- Top 20 highest rated movies
- Best movies by decade
- Top movies by specific genre
- Complete filmography of directors in Top 250

## Installation

1. Clone the repository:
```bash
git clone https://github.com/prettycoolflacko/MovieRecommendation.git
cd MovieRecommendation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Dataset

The application uses `imdb_top_250_movies_with_ratings.csv` which contains:
- **title**: Movie name
- **year**: Release year
- **duration**: Movie runtime
- **rating**: IMDB rating (1-10)
- **genres**: All genres (comma-separated)
- **directors**: Director name(s)
- **stars**: Top 3 cast members

## Technology Stack

- **Streamlit**: Web framework
- **Pandas**: Data manipulation
- **Plotly**: Interactive visualizations
- **Python 3.11+**

## Usage

Navigate through different pages using the sidebar:
- Use filters to find movies matching your preferences
- Explore analytics to discover trends
- Compare your favorite movies
- Browse curated top lists

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Data scraped from IMDB Top 250
