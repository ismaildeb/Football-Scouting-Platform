from pathlib import Path
import gc
import json

import pandas as pd


WINGER_POSITIONS = {
    "Left Wing",
    "Right Wing",
    "Left Midfield",
    "Right Midfield",
}

EVENT_COLS = [
    "match_id",
    "minute",
    "type.name",
    "player.id",
    "player.name",
    "team.name",
    "location",
    "pass.length",
    "pass.end_location",
    "carry.end_location",
    "shot.statsbomb_xg",
    "dribble.outcome.name",
]


def parse_match_id(file: Path) -> int:
    try:
        return int(file.stem)
    except ValueError as exc:
        raise ValueError(
            f"StatsBomb filename must contain a numeric match id: {file.name}"
        ) from exc


def load_wingers_from_lineups(lineups_dir: Path) -> pd.DataFrame:
    rows = []
    for file in lineups_dir.glob("*.json"):
        match_id = parse_match_id(file)
        data = json.loads(file.read_text(encoding="utf-8"))

        for team in data:
            team_name = team.get("team_name")
            for player in team.get("lineup", []):
                for pos in player.get("positions", []):
                    if pos.get("position") in WINGER_POSITIONS:
                        rows.append(
                            {
                                "match_id": match_id,
                                "player_id": player.get("player_id"),
                                "player_name": player.get("player_name"),
                                "team_name": team_name,
                                "position": pos.get("position"),
                                "start_minute": pos.get("from"),
                                "end_minute": pos.get("to"),
                            }
                        )

    columns = [
        "match_id",
        "player_id",
        "player_name",
        "team_name",
        "position",
        "start_minute",
        "end_minute",
    ]
    df = pd.DataFrame(rows, columns=columns)
    df["match_id"] = pd.to_numeric(df["match_id"], errors="coerce").astype("Int64")
    df["player_id"] = pd.to_numeric(df["player_id"], errors="coerce").astype("Int64")
    df["start_minute"] = pd.to_numeric(df["start_minute"], errors="coerce").fillna(0)
    df["end_minute"] = pd.to_numeric(df["end_minute"], errors="coerce").fillna(130)
    df = df.dropna(subset=["match_id", "player_id"]).reset_index(drop=True)
    return df


def build_events_light(events_dir: Path) -> pd.DataFrame:
    parts = []
    files = sorted(events_dir.glob("*.json"))

    for i, file in enumerate(files, start=1):
        match_id = parse_match_id(file)
        events = json.loads(file.read_text(encoding="utf-8"))
        df = pd.json_normalize(events)
        df["match_id"] = match_id

        existing = [c for c in EVENT_COLS if c in df.columns]
        part = df[existing].copy()
        missing = [c for c in EVENT_COLS if c not in part.columns]
        for c in missing:
            part[c] = pd.NA
        part = part[EVENT_COLS]
        parts.append(part)

        if i % 200 == 0:
            gc.collect()

    return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=EVENT_COLS)


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    data_dir = root / "data"

    events_dir = data_dir / "raw" / "statsbomb" / "events"
    lineups_dir = data_dir / "raw" / "statsbomb" / "lineups"
    processed = data_dir / "processed"
    processed.mkdir(parents=True, exist_ok=True)

    if not events_dir.exists():
        raise FileNotFoundError(f"Events directory not found: {events_dir}")
    if not lineups_dir.exists():
        raise FileNotFoundError(f"Lineups directory not found: {lineups_dir}")

    out_events_light = processed / "events_light.parquet"
    out_winger_events = processed / "winger_events.parquet"

    print("Building events_light with end_location columns...")
    df_events = build_events_light(events_dir)
    df_events.to_parquet(out_events_light, index=False)
    print(f"Saved: {out_events_light}")

    print("Loading winger intervals...")
    df_wingers = load_wingers_from_lineups(lineups_dir)

    print("Merging and filtering winger events...")
    df_events = df_events.rename(
        columns={
            "player.id": "player_id",
            "player.name": "player_name",
            "team.name": "team_name",
        }
    )
    df_events["match_id"] = pd.to_numeric(df_events["match_id"], errors="coerce").astype("Int64")
    df_events["player_id"] = pd.to_numeric(df_events["player_id"], errors="coerce").astype("Int64")
    df_events["minute"] = pd.to_numeric(df_events["minute"], errors="coerce")

    merged = df_events.merge(df_wingers, on=["match_id", "player_id"], how="inner", suffixes=("", "_winger"))
    merged = merged[(merged["minute"] >= merged["start_minute"]) & (merged["minute"] <= merged["end_minute"])]
    merged.to_parquet(out_winger_events, index=False)
    print(f"Saved: {out_winger_events}")
    print(f"Shape: {merged.shape}")


if __name__ == "__main__":
    main()
