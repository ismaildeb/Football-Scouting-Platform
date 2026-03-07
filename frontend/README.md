# Winger Dashboard

## Run
From project root:

```powershell
pip install -r requirements.txt
streamlit run frontend/app.py
```

## Data Inputs
Dashboard reads files from `data/processed`:

- `winger_role_scores_v2.parquet` (fallback: `winger_role_scores.parquet`)
- `winger_profiles.parquet` (optional)
- `winger_similar_players.parquet` (optional)
- `team_fit_shortlists.csv` (optional)
- `shortlist_*_v2.csv` (fallback: `shortlist_*.csv`)

