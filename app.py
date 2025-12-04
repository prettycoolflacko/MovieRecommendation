import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

# Page configuration
st.set_page_config(
    page_title="IMDB Top 250 Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #E50914;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #E50914;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .movie-card {
        background-color: #1a1a1a;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #E50914;
        color: #ffffff;
    }
    .movie-card h3, .movie-card h4 {
        color: #E50914;
        margin-bottom: 0.5rem;
    }
    .movie-card p {
        color: #e0e0e0;
        margin: 0.3rem 0;
    }
    .stat-card {
        background: #000000;
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        border: 2px solid #E50914;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('imdb_top_250_movies_with_ratings.csv')
    return df

df = load_data()

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/69/IMDB_Logo_2016.svg", width=200)
    st.markdown("---")
    
    page = st.radio("Navigation", [
        "🏠 Home",
        "🎯 Movie Quiz",
        "🔍 Find Movies",
        "📊 Analytics",
        "🎭 Compare Movies",
        "⭐ Top Lists"
    ])
    
    st.markdown("---")
    st.markdown("### About")
    st.info("Explore IMDB's Top 250 movies with advanced filtering, recommendations, and analytics.")

# Home Page
if page == "🏠 Home":
    st.markdown('<h1 class="main-header">🎬 IMDB Top 250 Movie Recommender</h1>', unsafe_allow_html=True)
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Total Movies", len(df))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Avg Rating", f"{df['rating'].mean():.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Year Range", f"{df['year'].min()}-{df['year'].max()}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        all_genres = ', '.join(df['genres'].dropna()).split(', ')
        st.metric("Unique Genres", len(set(all_genres)))
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Featured Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h2 class="sub-header">🏆 Top Rated Movies</h2>', unsafe_allow_html=True)
        top_5 = df.nlargest(5, 'rating')[['title', 'year', 'rating', 'genres']]
        for idx, row in top_5.iterrows():
            st.markdown(f"""
            <div class="movie-card">
                <h3>{row['title']} ({row['year']})</h3>
                <p>⭐ Rating: {row['rating']}</p>
                <p>🎭 Genres: {row['genres']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h2 class="sub-header">🎬 Recent Additions</h2>', unsafe_allow_html=True)
        recent_5 = df.nlargest(5, 'year')[['title', 'year', 'rating', 'genres']]
        for idx, row in recent_5.iterrows():
            st.markdown(f"""
            <div class="movie-card">
                <h3>{row['title']} ({row['year']})</h3>
                <p>⭐ Rating: {row['rating']}</p>
                <p>🎭 Genres: {row['genres']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Quick Stats Visualization
    st.markdown("---")
    st.markdown('<h2 class="sub-header">📈 Quick Insights</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Movies per decade
        df['decade'] = (df['year'] // 10) * 10
        decade_counts = df['decade'].value_counts().sort_index()
        fig = px.bar(x=decade_counts.index, y=decade_counts.values,
                     labels={'x': 'Decade', 'y': 'Number of Movies'},
                     title='Movies by Decade')
        fig.update_traces(marker_color='#E50914')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Rating distribution
        fig = px.histogram(df, x='rating', nbins=20,
                          labels={'rating': 'Rating', 'count': 'Number of Movies'},
                          title='Rating Distribution')
        fig.update_traces(marker_color='#764ba2')
        st.plotly_chart(fig, use_container_width=True)

# Movie Quiz Page
elif page == "🎯 Movie Quiz":
    st.markdown('<h1 class="main-header">🎯 Find Your Perfect Movie</h1>', unsafe_allow_html=True)
    st.markdown("### Answer a few questions to get personalized movie recommendations!")
    
    # Initialize session state
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    
    # Quiz form
    with st.form("movie_quiz"):
        st.markdown("#### 1️⃣ What's your mood today?")
        mood = st.radio(
            "Select your mood:",
            ["Excited & Energetic", "Thoughtful & Reflective", "Relaxed & Casual", "Tense & Thrilling", "Romantic & Emotional"],
            key="mood"
        )
        
        st.markdown("#### 2️⃣ What type of story interests you?")
        story_type = st.multiselect(
            "Choose up to 3 story types:",
            ["Action & Adventure", "Mystery & Crime", "Romance & Drama", "Comedy & Fun", 
             "Science Fiction & Fantasy", "Historical & Period", "Thriller & Suspense", 
             "War & Military", "Biography & Real Stories"],
            max_selections=3,
            key="story_type"
        )
        
        st.markdown("#### 3️⃣ How much time do you have?")
        duration_pref = st.radio(
            "Movie length preference:",
            ["Quick watch (< 2 hours)", "Standard (2-3 hours)", "Epic experience (> 3 hours)", "Any length"],
            key="duration"
        )
        
        st.markdown("#### 4️⃣ When do you prefer movies from?")
        era = st.radio(
            "Time period:",
            ["Classic (Before 1980)", "Golden Age (1980-1999)", "Modern (2000-2009)", "Recent (2010+)", "Any era"],
            key="era"
        )
        
        st.markdown("#### 5️⃣ What rating range are you looking for?")
        rating_pref = st.slider(
            "Minimum rating:",
            float(df['rating'].min()), 
            float(df['rating'].max()),
            8.0,
            0.1,
            key="rating"
        )
        
        st.markdown("#### 6️⃣ Do you have a favorite director?")
        all_directors = set()
        for directors in df['directors'].dropna():
            all_directors.update([d.strip() for d in directors.split(',')])
        
        favorite_director = st.selectbox(
            "Select a director (optional):",
            ["Any"] + sorted(list(all_directors)),
            key="director"
        )
        
        st.markdown("#### 7️⃣ Any specific actor you'd like to see?")
        actor_search = st.text_input(
            "Enter actor name (optional):",
            key="actor"
        )
        
        # Submit button
        submitted = st.form_submit_button("🎬 Get My Recommendations!", use_container_width=True)
        
        if submitted:
            st.session_state.quiz_completed = True
            st.session_state.quiz_answers = {
                'mood': mood,
                'story_type': story_type,
                'duration': duration_pref,
                'era': era,
                'rating': rating_pref,
                'director': favorite_director,
                'actor': actor_search
            }
    
    # Show recommendations if quiz completed
    if st.session_state.quiz_completed:
        st.markdown("---")
        st.markdown('<h2 class="sub-header">🎯 Your Personalized Recommendations</h2>', unsafe_allow_html=True)
        
        answers = st.session_state.quiz_answers
        
        # Filter movies based on answers
        filtered_movies = df.copy()
        
        # 1. Map mood to genres
        mood_genre_map = {
            "Excited & Energetic": ["Action", "Adventure", "Thriller"],
            "Thoughtful & Reflective": ["Drama", "Biography", "Historical"],
            "Relaxed & Casual": ["Comedy", "Romance", "Family"],
            "Tense & Thrilling": ["Thriller", "Crime", "Mystery", "Horror"],
            "Romantic & Emotional": ["Romance", "Drama", "Musical"]
        }
        
        mood_genres = mood_genre_map.get(answers['mood'], [])
        if mood_genres:
            filtered_movies = filtered_movies[filtered_movies['genres'].apply(
                lambda x: any(genre.lower() in str(x).lower() for genre in mood_genres)
            )]
        
        # 2. Filter by story type
        if answers['story_type']:
            story_genre_map = {
                "Action & Adventure": ["Action", "Adventure"],
                "Mystery & Crime": ["Mystery", "Crime", "Detective"],
                "Romance & Drama": ["Romance", "Drama", "Romantic"],
                "Comedy & Fun": ["Comedy"],
                "Science Fiction & Fantasy": ["Sci-Fi", "Fantasy", "Science Fiction"],
                "Historical & Period": ["Historical", "Period", "Epic", "History"],
                "Thriller & Suspense": ["Thriller", "Suspense", "Psychological"],
                "War & Military": ["War", "Military"],
                "Biography & Real Stories": ["Biography", "Biopic", "Docudrama"]
            }
            
            story_genres = []
            for story in answers['story_type']:
                story_genres.extend(story_genre_map.get(story, []))
            
            if story_genres:
                filtered_movies = filtered_movies[filtered_movies['genres'].apply(
                    lambda x: any(genre.lower() in str(x).lower() for genre in story_genres)
                )]
        
        # 3. Filter by duration
        if answers['duration'] != "Any length":
            if answers['duration'] == "Quick watch (< 2 hours)":
                filtered_movies = filtered_movies[filtered_movies['duration'].apply(
                    lambda x: 'h' in str(x) and int(str(x).split('h')[0]) < 2
                )]
            elif answers['duration'] == "Standard (2-3 hours)":
                filtered_movies = filtered_movies[filtered_movies['duration'].apply(
                    lambda x: 'h' in str(x) and 2 <= int(str(x).split('h')[0]) <= 3
                )]
            elif answers['duration'] == "Epic experience (> 3 hours)":
                filtered_movies = filtered_movies[filtered_movies['duration'].apply(
                    lambda x: 'h' in str(x) and int(str(x).split('h')[0]) > 3
                )]
        
        # 4. Filter by era
        if answers['era'] != "Any era":
            if answers['era'] == "Classic (Before 1980)":
                filtered_movies = filtered_movies[filtered_movies['year'] < 1980]
            elif answers['era'] == "Golden Age (1980-1999)":
                filtered_movies = filtered_movies[(filtered_movies['year'] >= 1980) & (filtered_movies['year'] < 2000)]
            elif answers['era'] == "Modern (2000-2009)":
                filtered_movies = filtered_movies[(filtered_movies['year'] >= 2000) & (filtered_movies['year'] < 2010)]
            elif answers['era'] == "Recent (2010+)":
                filtered_movies = filtered_movies[filtered_movies['year'] >= 2010]
        
        # 5. Filter by rating
        filtered_movies = filtered_movies[filtered_movies['rating'] >= answers['rating']]
        
        # 6. Filter by director
        if answers['director'] != "Any":
            filtered_movies = filtered_movies[filtered_movies['directors'].str.contains(
                answers['director'], case=False, na=False
            )]
        
        # 7. Filter by actor
        if answers['actor']:
            filtered_movies = filtered_movies[filtered_movies['stars'].str.contains(
                answers['actor'], case=False, na=False
            )]
        
        # Sort by rating
        filtered_movies = filtered_movies.sort_values('rating', ascending=False)
        
        # Display results
        st.markdown(f"### 🎬 Found {len(filtered_movies)} movies matching your preferences!")
        
        if len(filtered_movies) > 0:
            # Show top recommendations
            top_recommendations = filtered_movies.head(10)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("#### 🏆 Top Recommendations")
            with col2:
                if st.button("🔄 Reset Quiz"):
                    st.session_state.quiz_completed = False
                    st.session_state.quiz_answers = {}
                    st.rerun()
            
            for idx, (i, row) in enumerate(top_recommendations.iterrows(), 1):
                st.markdown(f"""
                <div class="movie-card">
                    <h3>#{idx} - {row['title']} ({row['year']})</h3>
                    <p><strong>⭐ Rating:</strong> {row['rating']}</p>
                    <p><strong>🎭 Genres:</strong> {row['genres']}</p>
                    <p><strong>🎬 Director:</strong> {row['directors']}</p>
                    <p><strong>⭐ Stars:</strong> {row['stars']}</p>
                    <p><strong>⏱️ Duration:</strong> {row['duration']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Show match breakdown
            st.markdown("---")
            st.markdown("#### 📊 Your Preference Summary")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info(f"**Mood:** {answers['mood']}")
                st.info(f"**Era:** {answers['era']}")
            
            with col2:
                story_types = ', '.join(answers['story_type']) if answers['story_type'] else "Any"
                st.info(f"**Story Types:** {story_types}")
                st.info(f"**Min Rating:** {answers['rating']}")
            
            with col3:
                st.info(f"**Duration:** {answers['duration']}")
                director_display = answers['director'] if answers['director'] != "Any" else "Any"
                st.info(f"**Director:** {director_display}")
            
            # Download option
            st.markdown("---")
            csv = filtered_movies.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download All Recommendations as CSV",
                data=csv,
                file_name="my_movie_recommendations.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.warning("😅 No movies found matching all your preferences. Try adjusting your answers!")
            if st.button("🔄 Try Again"):
                st.session_state.quiz_completed = False
                st.session_state.quiz_answers = {}
                st.rerun()

# Find Movies Page
elif page == "🔍 Find Movies":
    st.markdown('<h1 class="main-header">🔍 Find Your Perfect Movie</h1>', unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Genre filter
        all_genres = set()
        for genres in df['genres'].dropna():
            all_genres.update([g.strip() for g in genres.split(',')])
        all_genres = sorted(list(all_genres))
        
        selected_genres = st.multiselect("Select Genres", all_genres, default=[])
    
    with col2:
        # Year range
        year_range = st.slider("Year Range", 
                               int(df['year'].min()), 
                               int(df['year'].max()),
                               (int(df['year'].min()), int(df['year'].max())))
    
    with col3:
        # Rating filter
        min_rating = st.slider("Minimum Rating", 
                              float(df['rating'].min()), 
                              float(df['rating'].max()),
                              float(df['rating'].min()))
    
    # Search box
    search_term = st.text_input("🔎 Search by title, director, or actor", "")
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_genres:
        filtered_df = filtered_df[filtered_df['genres'].apply(
            lambda x: any(genre in str(x) for genre in selected_genres)
        )]
    
    filtered_df = filtered_df[
        (filtered_df['year'] >= year_range[0]) & 
        (filtered_df['year'] <= year_range[1]) &
        (filtered_df['rating'] >= min_rating)
    ]
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df['title'].str.contains(search_term, case=False, na=False) |
            filtered_df['directors'].str.contains(search_term, case=False, na=False) |
            filtered_df['stars'].str.contains(search_term, case=False, na=False)
        ]
    
    # Display results
    st.markdown(f"### Found {len(filtered_df)} movies")
    
    if len(filtered_df) > 0:
        # Sort options
        sort_by = st.selectbox("Sort by", ["Rating (High to Low)", "Rating (Low to High)", 
                                           "Year (Newest)", "Year (Oldest)", "Title (A-Z)"])
        
        if sort_by == "Rating (High to Low)":
            filtered_df = filtered_df.sort_values('rating', ascending=False)
        elif sort_by == "Rating (Low to High)":
            filtered_df = filtered_df.sort_values('rating', ascending=True)
        elif sort_by == "Year (Newest)":
            filtered_df = filtered_df.sort_values('year', ascending=False)
        elif sort_by == "Year (Oldest)":
            filtered_df = filtered_df.sort_values('year', ascending=True)
        else:
            filtered_df = filtered_df.sort_values('title')
        
        # Display movies
        for idx, row in filtered_df.iterrows():
            with st.expander(f"⭐ {row['rating']} | {row['title']} ({row['year']})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**🎭 Genres:** {row['genres']}")
                    st.markdown(f"**🎬 Director:** {row['directors']}")
                    st.markdown(f"**⭐ Stars:** {row['stars']}")
                    st.markdown(f"**⏱️ Duration:** {row['duration']}")
                
                with col2:
                    st.metric("Rating", row['rating'])
                    st.metric("Year", row['year'])
        
        # Download option
        st.markdown("---")
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name="filtered_movies.csv",
            mime="text/csv"
        )
    else:
        st.warning("No movies found with the selected filters. Try adjusting your criteria.")

# Analytics Page
elif page == "📊 Analytics":
    st.markdown('<h1 class="main-header">📊 Movie Analytics</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🎭 Genres", "🎬 Directors", "⭐ Ratings"])
    
    with tab1:
        st.markdown("### Year-based Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Movies over time
            df['decade'] = (df['year'] // 10) * 10
            movies_per_year = df.groupby('year').size().reset_index(name='count')
            fig = px.line(movies_per_year, x='year', y='count',
                         title='Number of Top 250 Movies by Year',
                         labels={'year': 'Year', 'count': 'Number of Movies'})
            fig.update_traces(line_color='#E50914')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Average rating by decade
            avg_rating_decade = df.groupby('decade')['rating'].mean().reset_index()
            fig = px.bar(avg_rating_decade, x='decade', y='rating',
                        title='Average Rating by Decade',
                        labels={'decade': 'Decade', 'rating': 'Average Rating'})
            fig.update_traces(marker_color='#764ba2')
            st.plotly_chart(fig, use_container_width=True)
        
        # Duration analysis
        st.markdown("### Duration Analysis")
        fig = px.box(df, y='duration',
                    title='Movie Duration Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Genre Analysis")
        
        # Count all genres
        all_genres = []
        for genres in df['genres'].dropna():
            all_genres.extend([g.strip() for g in genres.split(',')])
        
        genre_counts = Counter(all_genres)
        top_20_genres = dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:20])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top genres bar chart
            fig = px.bar(x=list(top_20_genres.keys()), y=list(top_20_genres.values()),
                        title='Top 20 Most Common Genres',
                        labels={'x': 'Genre', 'y': 'Count'})
            fig.update_traces(marker_color='#E50914')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Genre distribution pie chart (top 10)
            top_10_genres = dict(list(top_20_genres.items())[:10])
            fig = px.pie(values=list(top_10_genres.values()), 
                        names=list(top_10_genres.keys()),
                        title='Top 10 Genres Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        # Genre combinations
        st.markdown("### Popular Genre Combinations")
        genre_combo_counts = df['genres'].value_counts().head(10)
        st.dataframe(genre_combo_counts.reset_index().rename(
            columns={'index': 'Genre Combination', 'genres': 'Count'}
        ), use_container_width=True)
    
    with tab3:
        st.markdown("### Director Analysis")
        
        # Top directors
        all_directors = []
        for directors in df['directors'].dropna():
            all_directors.extend([d.strip() for d in directors.split(',')])
        
        director_counts = Counter(all_directors)
        top_directors = dict(sorted(director_counts.items(), key=lambda x: x[1], reverse=True)[:15])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top directors chart
            fig = px.bar(x=list(top_directors.keys()), y=list(top_directors.values()),
                        title='Directors with Most Movies in Top 250',
                        labels={'x': 'Director', 'y': 'Number of Movies'})
            fig.update_traces(marker_color='#667eea')
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Director average ratings
            director_ratings = {}
            for idx, row in df.iterrows():
                if pd.notna(row['directors']):
                    for director in row['directors'].split(','):
                        director = director.strip()
                        if director not in director_ratings:
                            director_ratings[director] = []
                        director_ratings[director].append(row['rating'])
            
            # Filter directors with at least 2 movies
            director_avg = {d: sum(ratings)/len(ratings) 
                          for d, ratings in director_ratings.items() 
                          if len(ratings) >= 2}
            top_rated_directors = dict(sorted(director_avg.items(), 
                                            key=lambda x: x[1], reverse=True)[:10])
            
            fig = px.bar(x=list(top_rated_directors.keys()), 
                        y=list(top_rated_directors.values()),
                        title='Top 10 Directors by Average Rating (min 2 movies)',
                        labels={'x': 'Director', 'y': 'Average Rating'})
            fig.update_traces(marker_color='#764ba2')
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### Rating Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Rating distribution
            fig = px.histogram(df, x='rating', nbins=30,
                             title='Rating Distribution',
                             labels={'rating': 'Rating', 'count': 'Count'})
            fig.update_traces(marker_color='#E50914')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Rating vs Year scatter
            fig = px.scatter(df, x='year', y='rating',
                           title='Rating vs Year',
                           labels={'year': 'Year', 'rating': 'Rating'},
                           hover_data=['title'])
            fig.update_traces(marker=dict(color='#764ba2', size=8))
            st.plotly_chart(fig, use_container_width=True)
        
        # Statistics
        st.markdown("### Rating Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Mean", f"{df['rating'].mean():.2f}")
        with col2:
            st.metric("Median", f"{df['rating'].median():.2f}")
        with col3:
            st.metric("Std Dev", f"{df['rating'].std():.2f}")
        with col4:
            st.metric("Range", f"{df['rating'].min():.1f} - {df['rating'].max():.1f}")

# Compare Movies Page
elif page == "🎭 Compare Movies":
    st.markdown('<h1 class="main-header">🎭 Compare Movies</h1>', unsafe_allow_html=True)
    
    st.markdown("### Select movies to compare")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        movie1 = st.selectbox("Movie 1", df['title'].sort_values())
    
    with col2:
        movie2 = st.selectbox("Movie 2", df['title'].sort_values(), index=1)
    
    with col3:
        movie3 = st.selectbox("Movie 3 (Optional)", ["None"] + df['title'].sort_values().tolist())
    
    # Get movie data
    movies_to_compare = [movie1, movie2]
    if movie3 != "None":
        movies_to_compare.append(movie3)
    
    comparison_df = df[df['title'].isin(movies_to_compare)]
    
    # Display comparison
    st.markdown("---")
    
    # Basic info comparison
    st.markdown("### Basic Information")
    
    cols = st.columns(len(movies_to_compare))
    
    for idx, (col, movie) in enumerate(zip(cols, movies_to_compare)):
        movie_data = comparison_df[comparison_df['title'] == movie].iloc[0]
        
        with col:
            st.markdown(f"""
            <div class="movie-card">
                <h3>{movie_data['title']}</h3>
                <p><strong>Year:</strong> {movie_data['year']}</p>
                <p><strong>Rating:</strong> ⭐ {movie_data['rating']}</p>
                <p><strong>Duration:</strong> {movie_data['duration']}</p>
                <p><strong>Genres:</strong> {movie_data['genres']}</p>
                <p><strong>Director:</strong> {movie_data['directors']}</p>
                <p><strong>Stars:</strong> {movie_data['stars']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Visual comparison
    st.markdown("### Visual Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Rating comparison
        fig = px.bar(comparison_df, x='title', y='rating',
                    title='Rating Comparison',
                    labels={'title': 'Movie', 'rating': 'Rating'})
        fig.update_traces(marker_color=['#E50914', '#667eea', '#764ba2'][:len(movies_to_compare)])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Year comparison
        fig = px.bar(comparison_df, x='title', y='year',
                    title='Release Year Comparison',
                    labels={'title': 'Movie', 'year': 'Year'})
        fig.update_traces(marker_color=['#764ba2', '#E50914', '#667eea'][:len(movies_to_compare)])
        st.plotly_chart(fig, use_container_width=True)

# Top Lists Page
elif page == "⭐ Top Lists":
    st.markdown('<h1 class="main-header">⭐ Top Lists</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 Top Rated", "📅 By Decade", "🎭 By Genre", "🎬 By Director"])
    
    with tab1:
        st.markdown("### Top 20 Highest Rated Movies")
        
        top_20 = df.nlargest(20, 'rating')[['title', 'year', 'rating', 'genres', 'directors']]
        
        for idx, (i, row) in enumerate(top_20.iterrows(), 1):
            with st.expander(f"#{idx} - {row['title']} ({row['year']}) - ⭐ {row['rating']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**Genres:** {row['genres']}")
                    st.markdown(f"**Director:** {row['directors']}")
                with col2:
                    st.metric("Rating", row['rating'])
    
    with tab2:
        st.markdown("### Top Movies by Decade")
        
        decade = st.selectbox("Select Decade", 
                             sorted(df['year'].apply(lambda x: (x // 10) * 10).unique(), reverse=True))
        
        decade_movies = df[df['year'].apply(lambda x: (x // 10) * 10) == decade]
        decade_movies = decade_movies.sort_values('rating', ascending=False).head(10)
        
        for idx, (i, row) in enumerate(decade_movies.iterrows(), 1):
            st.markdown(f"""
            <div class="movie-card">
                <h4>#{idx} - {row['title']} ({row['year']})</h4>
                <p>⭐ Rating: {row['rating']} | 🎭 {row['genres']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Top Movies by Genre")
        
        all_genres = set()
        for genres in df['genres'].dropna():
            all_genres.update([g.strip() for g in genres.split(',')])
        
        selected_genre = st.selectbox("Select Genre", sorted(list(all_genres)))
        
        genre_movies = df[df['genres'].str.contains(selected_genre, na=False)]
        genre_movies = genre_movies.sort_values('rating', ascending=False).head(10)
        
        for idx, (i, row) in enumerate(genre_movies.iterrows(), 1):
            st.markdown(f"""
            <div class="movie-card">
                <h4>#{idx} - {row['title']} ({row['year']})</h4>
                <p>⭐ Rating: {row['rating']} | 🎬 Director: {row['directors']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### Movies by Director")
        
        all_directors = set()
        for directors in df['directors'].dropna():
            all_directors.update([d.strip() for d in directors.split(',')])
        
        selected_director = st.selectbox("Select Director", sorted(list(all_directors)))
        
        director_movies = df[df['directors'].str.contains(selected_director, case=False, na=False)]
        director_movies = director_movies.sort_values('rating', ascending=False)
        
        st.markdown(f"**{selected_director}** has **{len(director_movies)}** movie(s) in Top 250")
        
        for idx, (i, row) in enumerate(director_movies.iterrows(), 1):
            st.markdown(f"""
            <div class="movie-card">
                <h4>{row['title']} ({row['year']})</h4>
                <p>⭐ Rating: {row['rating']} | 🎭 {row['genres']}</p>
                <p>⏱️ Duration: {row['duration']}</p>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Data source: IMDB Top 250 Movies | Built with Streamlit</p>
    <p>🎬 Discover your next favorite movie! 🎬</p>
</div>
""", unsafe_allow_html=True)
