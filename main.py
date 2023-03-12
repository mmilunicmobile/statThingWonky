import requests
import random
import matplotlib.pyplot as plt
import pandas as pd
import pathlib

data_csv = "fma-cal.csv"

# Sample the data if we haven't already
if not pathlib.Path(data_csv).exists():
    # Seed the pseudo-random number generator for repeatability
    random.seed(0)

    key = "o0COF8F9ueC9CQgGV43BRikJ8feKdM7KF4II3aW1ZtMwgqxua8V41w1Qs41HfNUX"

    fma_district_comps = requests.get(
        "https://www.thebluealliance.com/api/v3/district/2023fma/events/keys",
        headers={"X-TBA-Auth-Key": key},
    ).json()

    print("Has Districts")

    all_matches_fma = []

    for comp in fma_district_comps:
        all_matches_fma += requests.get(
            f"https://www.thebluealliance.com/api/v3/event/{comp}/matches/keys",
            headers={"X-TBA-Auth-Key": key},
        ).json()

    print("Has District Matches")

    california_comps = list(
        filter(
            lambda comp: comp["state_prov"] == "CA",
            requests.get(
                "https://www.thebluealliance.com/api/v3/events/2023/simple",
                headers={"X-TBA-Auth-Key": key},
            ).json(),
        )
    )

    print("Has California Comps")

    all_matches_cal = []

    for comp in california_comps:
        all_matches_cal += requests.get(
            f"https://www.thebluealliance.com/api/v3/event/{comp['key']}/matches/keys",
            headers={"X-TBA-Auth-Key": key},
        ).json()

    print("Has California Matches")

    california_samples = []

    n = 150

    while len(california_samples) < n:
        chosen_match = random.choice(all_matches_cal)
        data = requests.get(
            f"https://www.thebluealliance.com/api/v3/match/{chosen_match}/simple",
            headers={"X-TBA-Auth-Key": key},
        ).json()
        if data["actual_time"] == None:
            continue
        california_samples.append(
            max(data["alliances"]["blue"]["score"], data["alliances"]["red"]["score"])
        )
        print(f"Cal {len(california_samples)}")

    fma_samples = []

    while len(fma_samples) < n:
        chosen_match = random.choice(all_matches_fma)
        data = requests.get(
            f"https://www.thebluealliance.com/api/v3/match/{chosen_match}/simple",
            headers={"X-TBA-Auth-Key": key},
        ).json()
        if data["actual_time"] == None:
            continue
        fma_samples.append(
            max(data["alliances"]["blue"]["score"], data["alliances"]["red"]["score"])
        )
        print(f"Fma {len(fma_samples)}")

    dataframe = pd.DataFrame({"FMA": fma_samples, "CAL": california_samples})

    dataframe.to_csv(data_csv, index=False)

dataframe = pd.read_csv(data_csv)

print(dataframe.describe())

fma_samples = dataframe["FMA"]
california_samples = dataframe["CAL"]

# Graph both samples on boxplots
figure, axes = plt.subplots()
plt.xlabel("Winning Match Score (points)")
axes.boxplot([california_samples, fma_samples], 0, "rs", 0)
axes.set_yticklabels(["CAL", "FMA"])
figure.savefig("fma-cal-boxplot.png")
axes.clear()
