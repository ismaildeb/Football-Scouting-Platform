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
   
   # Run cells in each notebook:
   1. notebooks/extract_wingers.ipynb
   2. notebooks/wingers_features.ipynb
   3. notebooks/winger_profiles.ipynb
   4. notebooks/winger_shortlists.ipynb
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
├── notebooks/              # Jupyter notebooks for data processing
│   ├── extract_wingers.ipynb          # Extract winger events
│   ├── wingers_features.ipynb         # Calculate per90 metrics
│   ├── winger_profiles.ipynb          # PCA + Clustering
│   └── winger_shortlists.ipynb        # Role scoring
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
