# 🚀 How to Run This Platform

## Quick Start (5 minutes)

### Step 1: Clone the Repository

```bash
# Download the project from GitHub
git clone https://github.com/IsmailRach99/football-scouting-platform.git
cd football-scouting-platform
```

### Step 2: Install Dependencies

```bash
# Install all required Python packages
pip install -r requirements.txt
```

**What gets installed:**
- pandas, numpy (data analysis)
- pyarrow (parquet file support)
- plotly (interactive charts)
- streamlit (dashboard framework)
- scikit-learn (clustering algorithms)

### Step 3: Get Data

You have **two options**:

#### Option A: Use Your Own StatsBomb Data (Recommended for clubs/scouts)

1. Download free StatsBomb event data:
   - Go to: https://github.com/statsbomb/open-data
   - Download the `events` and `lineups` folders
   
2. Place data in the correct folders:
   ```
   football-scouting-platform/
   └── data/
       └── raw/
           └── statsbomb/
               ├── events/      ← Put JSON files here
               └── lineups/     ← Put JSON files here
   ```

3. Generate processed data files:
   ```bash
   # Open Jupyter and run these notebooks IN ORDER:
   jupyter notebook
   
   # Run cells in each notebook (8 total):
   1. notebooks/load_statsbomb_events.ipynb      # Load StatsBomb data
   2. notebooks/extract_wingers.ipynb            # Extract winger events
   3. notebooks/wingers_features.ipynb           # Basic per90 features
   4. notebooks/wingers_features_v2.ipynb        # Enhanced features (optional)
   5. notebooks/winger_profiles.ipynb            # PCA + Clustering
   6. notebooks/winger_shortlists.ipynb          # Basic role scoring
   7. notebooks/winger_shortlists_v2.ipynb       # Advanced scoring with stability
   8. notebooks/team_fit_recommender.ipynb       # Team-fit recommendations
   ```

#### Option B: Request Sample Data (For testing/demo)

If you just want to test the platform quickly, contact the author or check the releases section for pre-processed sample data files.

### Step 4: Run the Dashboard

```bash
# From the project root folder
streamlit run frontend/app.py
```

**This will:**
- Start a local web server
- Automatically open your browser at `http://localhost:8501`
- Display the Winger Scouting Dashboard!

---

## 📊 What You'll See in the Dashboard

### Tab 1: Overview
- Total players in database
- Cluster distribution chart
- Average minutes played
- Filter by cluster type and age cohort

### Tab 2: Player Explorer
- Search any player by name
- View their cluster assignment
- See percentile rankings (strengths)
- Role fit scores
- Similar players comparison

### Tab 3: Role Shortlists
- Top 50 Direct Runners
- Top 50 Playmaker Wingers
- Top 50 Inside Forwards
- Export to CSV for recruitment meetings

### Tab 4: Team Fit
- Tactical style matching
- Possession-based wingers
- Counter-attack specialists
- Direct play experts

---

## 🔧 Troubleshooting

### "No module named 'pandas'"
→ Run: `pip install -r requirements.txt`

### "FileNotFoundError: winger_role_scores.parquet"
→ You need to run the notebooks first (Step 3A above)

### "No players in current filter"
→ Check that you have data files in `data/processed/`
→ Try widening your filter ranges in the sidebar

### Dashboard won't open
→ Make sure port 8501 is not in use
→ Try: `streamlit run frontend/app.py --server.port 8502`

---

## 💻 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: ~10GB for StatsBomb data + 500MB for processed files
- **Browser**: Chrome, Firefox, Edge (any modern browser)

---

## 📁 Project Structure

```
football-scouting-platform/
├── notebooks/              # 8 Jupyter notebooks for data processing
│   ├── load_statsbomb_events.ipynb      # Load StatsBomb event data
│   ├── extract_wingers.ipynb            # Extract winger events from lineups
│   ├── wingers_features.ipynb           # Compute basic per90 metrics
│   ├── wingers_features_v2.ipynb        # Enhanced feature engineering
│   ├── winger_profiles.ipynb            # PCA + K-Means clustering
│   ├── winger_shortlists.ipynb          # Basic role-based scoring
│   ├── winger_shortlists_v2.ipynb       # Advanced role scoring
│   └── team_fit_recommender.ipynb       # Tactical fit analysis
├── frontend/               # Dashboard application
│   └── app.py                         # Streamlit app
├── data/
│   ├── raw/              # Raw StatsBomb data (YOU provide this)
│   └── processed/        # Generated parquet/CSV files
├── src/                  # Production Python modules
├── requirements.txt        # Dependencies list
└── README.md             # This documentation
```

---

## 🎯 Who Is This For?

### Football Clubs & Scouts
- Find undervalued wingers
- Identify tactical fits
- Compare players objectively
- Generate recruitment shortlists

### Data Analysts
- Learn football analytics pipeline
- Study clustering techniques
- Build similar platforms

### Students/Researchers
- Academic projects
- Sports science research
- Machine learning applications

---

## 🤝 Need Help?

**Issues with setup?** → Open an issue on GitHub  
**Questions about methodology?** → Contact: ismailrach99@gmail.com  
**Want to collaborate?** → Pull requests welcome!

---

## 📝 Notes

- **Data Privacy**: All StatsBomb data is open-source and freely available
- **License**: Check individual data sources for usage rights
- **Updates**: New features added regularly - check back for improvements!

---

*Happy scouting! ⚽🔍*
