import json
import tempfile
import unittest
from pathlib import Path

from src.features.rebuild_winger_events import (
    build_events_light,
    load_wingers_from_lineups,
    parse_match_id,
)


class RebuildWingerEventsTests(unittest.TestCase):
    def test_parse_match_id_rejects_non_numeric_filename(self):
        with self.assertRaisesRegex(ValueError, "match id"):
            parse_match_id(Path("not-a-match.json"))

    def test_build_events_light_preserves_schema_when_directory_is_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            events = build_events_light(Path(directory))

        self.assertTrue(events.empty)
        self.assertEqual(len(events.columns), 12)

    def test_load_wingers_from_lineups_extracts_winger_interval(self):
        with tempfile.TemporaryDirectory() as directory:
            lineup_file = Path(directory) / "123.json"
            lineup_file.write_text(
                json.dumps(
                    [
                        {
                            "team_name": "Example FC",
                            "lineup": [
                                {
                                    "player_id": 7,
                                    "player_name": "Test Winger",
                                    "positions": [
                                        {
                                            "position": "Right Wing",
                                            "from": 12,
                                            "to": 84,
                                        }
                                    ],
                                }
                            ],
                        }
                    ]
                ),
                encoding="utf-8",
            )

            wingers = load_wingers_from_lineups(Path(directory))

        self.assertEqual(len(wingers), 1)
        self.assertEqual(wingers.loc[0, "player_id"], 7)
        self.assertEqual(wingers.loc[0, "start_minute"], 12)
        self.assertEqual(wingers.loc[0, "end_minute"], 84)


if __name__ == "__main__":
    unittest.main()
