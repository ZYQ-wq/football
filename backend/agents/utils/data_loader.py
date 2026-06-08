import json
import os


def load_team_by_id(team_id: str):

    data_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data"
    )

    file_path = os.path.join(
        data_dir,
        f"{team_id}.json"
    )

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)