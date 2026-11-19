from pathlib import Path
from typing import Dict

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Winger Scouting Dashboard",
    page_icon="WS",
    layout="wide",
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"


def create_demo_data() -> Dict[str, pd.DataFrame]:
    names = [
        "Alex Morgan",
        "Theo Silva",
        "Liam Costa",
        "Noah Diallo",
        "Milan Reyes",
        "Lucas Bauer",
        "Enzo Martin",
        "Ibrahim Kane",
        "Leo Santos",
        "Yanis Morel",
        "Adam Rossi",
        "Elias Haddad",
    ]

    role_scores = pd.DataFrame(
        {
            "player_id": range(1001, 1013),
            "player_name": names,
            "cluster_name": [
                "Direct Attackers",
                "Creative Wingers",
                "Inside Forwards",
                "Direct Attackers",
                "Creative Wingers",
                "Inside Forwards",
                "Direct Attackers",
                "Creative Wingers",
                "Inside Forwards",
                "Direct Attackers",
                "Creative Wingers",
                "Inside Forwards",
            ],
            "minutes": [3200, 2950, 2800, 2600, 2450, 2300, 2100, 1950, 1800, 1650, 1500, 1200],
            "cluster_agreement": [0.91, 0.88, 0.86, 0.84, 0.82, 0.79, 0.77, 0.75, 0.73, 0.71, 0.68, 0.64],
            "age_cohort": [
                "U23",
                "23-27",
                "23-27",
                "U23",
                "28+",
                "23-27",
                "U23",
                "23-27",
                "28+",
                "U23",
                "23-27",
                "28+",
            ],
        }
    )

    for index in range(len(role_scores)):
        role_scores.loc[index, "score_direct_runner_adj"] = 55 + (index * 3) % 40
        role_scores.loc[index, "score_playmaker_winger_adj"] = 50 + (index * 7) % 45
        role_scores.loc[index, "score_inside_forward_adj"] = 48 + (index * 5) % 47
        role_scores.loc[index, "dribbles_pct"] = 50 + (index * 4) % 50
        role_scores.loc[index, "progressive_passes_pct"] = 45 + (index * 6) % 55
        role_scores.loc[index, "shots_pct"] = 40 + (index * 5) % 60
        role_scores.loc[index, "xg_pct"] = 45 + (index * 7) % 55
        role_scores.loc[index, "ball_carries_pct"] = 50 + (index * 3) % 50

    shortlists = {}
    for role in ["direct_runner", "playmaker_winger", "inside_forward"]:
        score_column = f"score_{role}_adj"
        shortlist = role_scores.nlargest(8, score_column)[
            ["player_id", "player_name", "minutes", "cluster_name", score_column]
        ].copy()
        shortlist["rank"] = range(1, len(shortlist) + 1)
        shortlists[role] = shortlist

    team_fit = pd.DataFrame(
        [
            {
                "team_style": style,
                "rank": rank,
                "player_id": int(row["player_id"]),
                "player_name": row["player_name"],
                "team_fit_score": round(float(row["score_direct_runner_adj"] if style == "counter_attack" else row["score_playmaker_winger_adj"]), 1),
            }
            for style in ["possession", "counter_attack", "direct"]
            for rank, (_, row) in enumerate(role_scores.iterrows(), start=1)
        ]
    )

    return {
        "role_scores": role_scores,
        "profiles": role_scores[
            ["player_id", "player_name", "cluster_name", "minutes", "cluster_agreement"]
        ].copy(),
        "similar": pd.DataFrame(),
        "team_fit": team_fit,
        "shortlists": shortlists,
    }


def read_optional_file(path: Path, reader) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return reader(path)
    except (FileNotFoundError, OSError, ValueError, pd.errors.EmptyDataError) as exc:
        st.warning(f"Could not read {path.name}: {exc}")
        return pd.DataFrame()


@st.cache_data
def load_data() -> Dict[str, pd.DataFrame]:
    data = {}

    role_scores_path = DATA_DIR / "winger_role_scores_v2.parquet"
    if not role_scores_path.exists():
        role_scores_path = DATA_DIR / "winger_role_scores.parquet"
    data["role_scores"] = read_optional_file(role_scores_path, pd.read_parquet)

    profiles_path = DATA_DIR / "winger_profiles.parquet"
    data["profiles"] = read_optional_file(profiles_path, pd.read_parquet)

    similar_path = DATA_DIR / "winger_similar_players.parquet"
    data["similar"] = read_optional_file(similar_path, pd.read_parquet)

    team_fit_path = DATA_DIR / "team_fit_shortlists.csv"
    data["team_fit"] = read_optional_file(team_fit_path, pd.read_csv)

    shortlists = {}
    for role in ["direct_runner", "playmaker_winger", "inside_forward"]:
        p = DATA_DIR / f"shortlist_{role}_v2.csv"
        if not p.exists():
            p = DATA_DIR / f"shortlist_{role}.csv"
        shortlists[role] = read_optional_file(p, pd.read_csv)
    data["shortlists"] = shortlists

    return data


data = load_data()
role_scores = data["role_scores"].copy()
profiles = data["profiles"].copy()
similar = data["similar"].copy()
team_fit = data["team_fit"].copy()
shortlists = data["shortlists"]
demo_mode = role_scores.empty

if demo_mode:
    data = create_demo_data()
    role_scores = data["role_scores"].copy()
    profiles = data["profiles"].copy()
    similar = data["similar"].copy()
    team_fit = data["team_fit"].copy()
    shortlists = data["shortlists"]

# Fallback name enrichment if role_scores is missing player_name
if "player_name" not in role_scores.columns and not profiles.empty and "player_id" in profiles.columns:
    name_cols = [c for c in ["player_name", "player_name_x", "player_name_y"] if c in profiles.columns]
    if name_cols:
        profile_names = (
            profiles[["player_id"] + name_cols]
            .copy()
            .assign(player_name=lambda x: x[name_cols].bfill(axis=1).iloc[:, 0])
            [["player_id", "player_name"]]
            .dropna(subset=["player_name"])
            .drop_duplicates(subset=["player_id"])
        )
        role_scores = role_scores.merge(profile_names, on="player_id", how="left")

st.title("Winger Scouting Platform")
st.caption("Recruitment-focused winger profiling, role scoring, and team-fit shortlisting")

if demo_mode:
    st.info(
        "Demo mode: synthetic players are shown because no processed role-score file "
        "was found. Add data/processed/winger_role_scores_v2.parquet to use real data."
    )

if "cluster_name" not in role_scores.columns:
    role_scores["cluster_name"] = "Unknown"
if "minutes" not in role_scores.columns:
    role_scores["minutes"] = 0
if "cluster_agreement" not in role_scores.columns:
    role_scores["cluster_agreement"] = 1.0
if "age_cohort" not in role_scores.columns:
    role_scores["age_cohort"] = "Unknown"

role_scores["minutes"] = pd.to_numeric(role_scores["minutes"], errors="coerce").fillna(0)
role_scores["cluster_agreement"] = pd.to_numeric(
    role_scores["cluster_agreement"], errors="coerce"
).fillna(0)

score_cols = [c for c in role_scores.columns if c.startswith("score_") and c.endswith("_adj")]
if not score_cols:
    score_cols = [c for c in role_scores.columns if c.startswith("score_")]

with st.sidebar:
    st.header("Filters")
    min_minutes = int(role_scores["minutes"].min())
    max_minutes = int(role_scores["minutes"].max())
    if min_minutes == max_minutes:
        st.caption(f"Minutes: {min_minutes:,} (all players)")
        minutes_range = (min_minutes, max_minutes)
    else:
        default_min = min(max(min_minutes, 300), max_minutes)
        minutes_range = st.slider(
            "Minutes",
            min_value=min_minutes,
            max_value=max_minutes,
            value=(default_min, max_minutes),
        )

    cluster_options = sorted(role_scores["cluster_name"].dropna().astype(str).unique().tolist())
    selected_clusters = st.multiselect("Cluster", cluster_options, default=cluster_options)

    cohort_options = sorted(role_scores["age_cohort"].dropna().astype(str).unique().tolist())
    selected_cohorts = st.multiselect("Age Cohort", cohort_options, default=cohort_options)

filtered = role_scores[
    (role_scores["minutes"] >= minutes_range[0])
    & (role_scores["minutes"] <= minutes_range[1])
    & (role_scores["cluster_name"].astype(str).isin(selected_clusters))
    & (role_scores["age_cohort"].astype(str).isin(selected_cohorts))
].copy()

tab_overview, tab_player, tab_shortlists, tab_teamfit = st.tabs(
    ["Overview", "Player Explorer", "Role Shortlists", "Team Fit"]
)

with tab_overview:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Players", f"{len(filtered):,}")
    c2.metric("Clusters", f"{filtered['cluster_name'].nunique():,}")
    c3.metric("Avg Minutes", f"{filtered['minutes'].mean():.0f}")
    c4.metric("Avg Stability", f"{filtered['cluster_agreement'].mean():.2f}")

    if not filtered.empty:
        cluster_count = (
            filtered["cluster_name"].value_counts().rename_axis("cluster_name").reset_index(name="players")
        )
        fig = px.bar(
            cluster_count,
            x="cluster_name",
            y="players",
            title="Players by Cluster",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Dataset Preview")
        st.dataframe(filtered.head(100), use_container_width=True)

with tab_player:
    if filtered.empty:
        st.warning("No players in current filter.")
    else:
        name_col = "player_name" if "player_name" in filtered.columns else "player_id"
        options = filtered[[name_col, "player_id"]].drop_duplicates()
        options["label"] = options[name_col].astype(str) + " (" + options["player_id"].astype(str) + ")"
        selected_label = st.selectbox("Select Player", options["label"].tolist())
        selected_id = int(options.loc[options["label"] == selected_label, "player_id"].iloc[0])

        player_row = filtered[filtered["player_id"] == selected_id].iloc[0]
        st.write(
            f"**Cluster:** {player_row.get('cluster_name', 'Unknown')} | "
            f"**Minutes:** {player_row.get('minutes', 0):.0f} | "
            f"**Stability:** {player_row.get('cluster_agreement', 1.0):.2f}"
        )

        pct_cols = [c for c in filtered.columns if c.endswith("_pct")]
        top_strengths = (
            pd.to_numeric(player_row[pct_cols], errors="coerce")
            .dropna()
            .rename(index=lambda c: c.replace("_pct", ""))
            .sort_values(ascending=False)
            .head(5)
        )
        if not top_strengths.empty:
            st.subheader("Top Strengths (Percentiles)")
            st.dataframe(top_strengths.rename("percentile").to_frame(), use_container_width=True)

        if score_cols:
            st.subheader("Role Fit Scores")
            role_scores_view = pd.to_numeric(player_row[score_cols], errors="coerce").dropna()
            if not role_scores_view.empty:
                role_scores_view.index = [
                    c.replace("score_", "").replace("_adj", "") for c in role_scores_view.index
                ]
                role_scores_view = (
                    role_scores_view.sort_values(ascending=False)
                    .rename("score")
                    .reset_index()
                    .rename(columns={"index": "role"})
                )
                fig_role = px.bar(role_scores_view, x="role", y="score", title="Role Fit")
                st.plotly_chart(fig_role, use_container_width=True)

        if not similar.empty and "player_id" in similar.columns:
            sp = similar[similar["player_id"] == selected_id].copy()
            if not sp.empty:
                st.subheader("Similar Players")
                st.dataframe(sp.head(20), use_container_width=True)

with tab_shortlists:
    role_label_map = {
        "direct_runner": "Direct Runner",
        "playmaker_winger": "Playmaker Winger",
        "inside_forward": "Inside Forward",
    }
    selected_role = st.selectbox("Select Role", list(role_label_map.keys()), format_func=lambda x: role_label_map[x])
    role_df = shortlists.get(selected_role, pd.DataFrame()).copy()

    if role_df.empty:
        st.warning("No shortlist file found for this role.")
    else:
        if "player_id" in filtered.columns and "player_id" in role_df.columns:
            role_df = role_df[role_df["player_id"].isin(filtered["player_id"])]
        st.dataframe(role_df.head(200), use_container_width=True)
        st.download_button(
            label="Download Role Shortlist CSV",
            data=role_df.to_csv(index=False).encode("utf-8"),
            file_name=f"shortlist_{selected_role}.csv",
            mime="text/csv",
        )

with tab_teamfit:
    if team_fit.empty or "team_style" not in team_fit.columns:
        st.warning("No team-fit shortlist file found.")
    else:
        styles = sorted(team_fit["team_style"].dropna().unique().tolist())
        selected_style = st.selectbox("Team Style", styles)
        tf = team_fit[team_fit["team_style"] == selected_style].copy()
        if "player_id" in filtered.columns and "player_id" in tf.columns:
            tf = tf[tf["player_id"].isin(filtered["player_id"])]
        st.dataframe(tf.head(200), use_container_width=True)
        st.download_button(
            label="Download Team Fit CSV",
            data=tf.to_csv(index=False).encode("utf-8"),
            file_name=f"team_fit_{selected_style}.csv",
            mime="text/csv",
        )


