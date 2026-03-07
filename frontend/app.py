from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Winger Scouting Dashboard",
    page_icon="WS",
    layout="wide",
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"


@st.cache_data
def load_data() -> dict[str, pd.DataFrame]:
    data = {}

    role_scores_path = DATA_DIR / "winger_role_scores_v2.parquet"
    if not role_scores_path.exists():
        role_scores_path = DATA_DIR / "winger_role_scores.parquet"
    data["role_scores"] = pd.read_parquet(role_scores_path)

    profiles_path = DATA_DIR / "winger_profiles.parquet"
    data["profiles"] = pd.read_parquet(profiles_path) if profiles_path.exists() else pd.DataFrame()

    similar_path = DATA_DIR / "winger_similar_players.parquet"
    data["similar"] = pd.read_parquet(similar_path) if similar_path.exists() else pd.DataFrame()

    team_fit_path = DATA_DIR / "team_fit_shortlists.csv"
    data["team_fit"] = pd.read_csv(team_fit_path) if team_fit_path.exists() else pd.DataFrame()

    shortlists = {}
    for role in ["direct_runner", "playmaker_winger", "inside_forward"]:
        p = DATA_DIR / f"shortlist_{role}_v2.csv"
        if not p.exists():
            p = DATA_DIR / f"shortlist_{role}.csv"
        shortlists[role] = pd.read_csv(p) if p.exists() else pd.DataFrame()
    data["shortlists"] = shortlists

    return data


data = load_data()
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

if role_scores.empty:
    st.error("No role scores file found. Run your feature/shortlist notebooks first.")
    st.stop()

if "cluster_name" not in role_scores.columns:
    role_scores["cluster_name"] = "Unknown"
if "minutes" not in role_scores.columns:
    role_scores["minutes"] = 0
if "cluster_agreement" not in role_scores.columns:
    role_scores["cluster_agreement"] = 1.0
if "age_cohort" not in role_scores.columns:
    role_scores["age_cohort"] = "Unknown"

score_cols = [c for c in role_scores.columns if c.startswith("score_") and c.endswith("_adj")]
if not score_cols:
    score_cols = [c for c in role_scores.columns if c.startswith("score_")]

with st.sidebar:
    st.header("Filters")
    min_minutes = int(role_scores["minutes"].min())
    max_minutes = int(role_scores["minutes"].max())
    minutes_range = st.slider(
        "Minutes",
        min_value=min_minutes,
        max_value=max_minutes,
        value=(max(min_minutes, 300), max_minutes),
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
            pd.Series({c.replace("_pct", ""): float(player_row[c]) for c in pct_cols})
            .sort_values(ascending=False)
            .head(5)
        )
        if not top_strengths.empty:
            st.subheader("Top Strengths (Percentiles)")
            st.dataframe(top_strengths.rename("percentile").to_frame(), use_container_width=True)

        if score_cols:
            st.subheader("Role Fit Scores")
            role_scores_view = (
                pd.Series({c.replace("score_", "").replace("_adj", ""): float(player_row[c]) for c in score_cols})
                .sort_values(ascending=False)
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
    if team_fit.empty:
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


