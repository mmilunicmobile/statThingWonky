import requests
import json
import random
import numpy

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

print("\tFMA\tCAL")
for a in enumerate(zip(fma_samples, california_samples)):
    print(f"{a[0]+1}.\t{a[1][0]}\t{a[1][1]}")

print("\n")
print("\tstd\tmean\tn")
print(
    f"FMA\t{numpy.std(fma_samples,ddof=1)}\t{numpy.mean(fma_samples)}\t{len(fma_samples)}"
)
print(
    f"CAL\t{numpy.std(california_samples,ddof=1)}\t{numpy.mean(california_samples)}\t{len(california_samples)}"
)
