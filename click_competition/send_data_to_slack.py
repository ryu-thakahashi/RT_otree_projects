import time
from pathlib import Path

import polars as pl
from filelock import FileLock
from icecream import ic
from slack_sdk import WebClient

DIR_PATH = Path(__file__).resolve()


def send_to_slack(data: dict, channel_id: str = "C08H9NBRFS9") -> None:
    with open(DIR_PATH.parent / "tk.txt", "r") as f:
        TK = "-".join(f.read().strip().split("\n"))

    date_now = time.strftime("%Y%m%d%H%M")
    csv_path = f"raw_data/{date_now}.csv"
    lock_path = csv_path + ".lock"
    lock = FileLock(lock_path)

    with lock:
        df = pl.DataFrame(data)
        df.write_csv(csv_path)

    client = WebClient(token=TK)
    res = client.files_upload_v2(
        channel=channel_id,
        file=csv_path,
    )


if __name__ == "__main__":
    send_to_slack({"id": [0, 1], "clicks": [39, 27]})
    ic("done")
