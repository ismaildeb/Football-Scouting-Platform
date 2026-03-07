# ⚽ Football Scouting Platform - Winger Analysis

A data-driven recruitment platform for identifying and analyzing winger profiles using advanced clustering and role-based scoring.

## 🎯 Purpose

This platform helps football clubs and scouts:
- **Discover wingers** matching specific tactical roles (Direct Runner, Playmaker Winger, Inside Forward)
- **Compare players** using standardized per90 metrics and percentile rankings
- **Find similar players** to targets using PCA-based similarity
- **Generate shortlists** filtered by team style and tactical fit

## 📊 Key Features

### 1. Role-Based Profiling
Players are scored and ranked for three distinct winger roles:
- **Direct Runner**: High dribbles + carries, drives at defenders
- **Playmaker Winger**: High passing + ball progression, creative outlet
- **Inside Forward**: High shots + xG, goal-scoring threat

### 2. Cluster Analysis
- PCA dimensionality reduction with silhouette score optimization
- K-Means clustering with stability validation (30+ runs)
- Automatic cluster naming based on statistical profiles

### 3. Player Comparison
- Similar player finder using Euclidean distance in PCA space
- Percentile rankings across 5 key metrics
- Strengths radar charts

### 4. Team Fit Recommendations
- Tactical style matching (possession, counter-attack, direct)
- Customizable weightings for role scores
- Export-ready shortlists

## 🏗️ Architecture

```
football-scouting-platform/
├── notebooks/              # Jupyter notebooks for analysis
│   ├── load_statsbomb_events.ipynb      # Load and process StatsBomb event data
│   ├── extract_wingers.ipynb            # Extract winger events from lineups
│   ├── wingers_features.ipynb           # Compute basic per90 features
│   ├── wingers_features_v2.ipynb        # Enhanced feature engineering
│   ├── winger_profiles.ipynb            # PCA + K-Means clustering
│   ├── winger_shortlists.ipynb          # Basic role-based scoring
│   ├── winger_shortlists_v2.ipynb       # Advanced role scoring with stability
│   └── team_fit_recommender.ipynb       # Team-fit recommendations
├── frontend/               # Streamlit dashboard
│   ├── app.py                         # Main dashboard application
│   └── README.md                      # Dashboard documentation
├── data/
│   ├── raw/              # Raw StatsBomb data (not tracked in git)
│   └── processed/        # Processed parquet files (not tracked in git)
├── src/                  # Production modules (future development)
│   ├── features/
│   ├── models/
│   └── api/
├── requirements.txt        # Python dependencies
└── .gitignore             # Git ignore rules
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd football-scouting-platform

# Install dependencies
pip install -r requirements.txt
```

### Run the Dashboard

```bash
# From project root directory
streamlit run frontend/app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Generate Data (First Time Setup)

Run the notebooks in order to generate the required data files:

```bash
# 1. Load StatsBomb event data
jupyter notebook notebooks/load_statsbomb_events.ipynb

# 2. Extract winger events from lineups
jupyter notebook notebooks/extract_wingers.ipynb

# 3. Compute basic per90 features
jupyter notebook notebooks/wingers_features.ipynb

# 4. Enhanced feature engineering (optional - v2)
jupyter notebook notebooks/wingers_features_v2.ipynb

# 5. Build clusters and profiles
jupyter notebook notebooks/winger_profiles.ipynb

# 6. Generate basic role-based shortlists
jupyter notebook notebooks/winger_shortlists.ipynb

# 7. Advanced role scoring with stability (v2)
jupyter notebook notebooks/winger_shortlists_v2.ipynb

# 8. Create team-fit recommendations
jupyter notebook notebooks/team_fit_recommender.ipynb
```

## 📈 Data Pipeline

1. **Data Ingestion**: StatsBomb event data (JSON) → Parquet
2. **Feature Engineering**: Per90 metrics (dribbles, carries, passes, shots, xG)
3. **Dimensionality Reduction**: PCA (85% variance target)
4. **Clustering**: K-Means with silhouette optimization
5. **Role Scoring**: Weighted composite scores for each role type
6. **Shortlists**: Top-N players per role with stability filtering

## 📊 Metrics Used

### Attacking Metrics
- Dribbles per90 (attempted + successful)
- Carries per90
- Passes per90
- Shots per90
- xG per90

### Advanced Metrics (Future)
- Progressive passes/carries
- Dribble success rate
- Defensive contributions
- Form trends

## 🔧 Configuration

Key parameters in notebooks:
- `MINUTES_MIN = 300` - Minimum playing time threshold
- `VARIANCE_TARGET = 0.85` - PCA variance explained
- `MIN_STABILITY = 0.60` - Cluster agreement threshold
- `TOP_N = 50` - Shortlist size per role

## 📦 Dependencies

See `requirements.txt`:
- pandas, numpy - Data manipulation
- pyarrow - Parquet file handling
- scikit-learn - PCA, K-Means, preprocessing
- plotly - Interactive visualizations
- streamlit - Dashboard framework
- jupyter - Notebook environment


## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional feature engineering (progressive metrics, defensive work)
- Age cohort analysis
- League strength adjustments
- Video integration
- API development



