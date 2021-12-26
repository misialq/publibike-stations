import sys

import pandas as pd
from requests import get

STATIONS_URL = "https://api.publibike.ch/v1/public/partner/stations"


def run():
    response = get(STATIONS_URL)
    stations = response.json().get("stations")

    retain_keys = [
        "id",
        "latitude",
        "longitude",
        "state",
        "name",
        "address",
        "zip",
        "city",
    ]
    stations_info = [{k: v for k, v in s.items() if k in retain_keys} for s in stations]

    for s in stations_info:
        state = s.pop("state")
        s["state"] = state["name"]

    stations_df = pd.DataFrame(stations_info)
    stations_df["state"] = stations_df["state"].replace("Active (empty)", "Active")
    stations_df.sort_values("id", inplace=True)
    stations_df.set_index("id", drop=True, inplace=True)

    if len(stations_df) > 0:
        stations_df.to_csv("./stations/stations.csv")
    else:
        sys.exit(1)


if __name__ == "__main__":
    run()
