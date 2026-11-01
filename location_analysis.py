"""
Location-based Analysis: city profile tool
Run: python location_analysis.py
Needs in the same folder: Dataset.csv
"""
from collections import Counter

import pandas as pd

NCR = ['New Delhi', 'Gurgaon', 'Noida', 'Faridabad', 'Ghaziabad']


def fix_city(name):
    if name.isascii():
        return name
    if name.endswith('stanbul'):
        return 'Istanbul'
    if name.startswith('S') and name.endswith('o Paulo'):
        return 'Sao Paulo'
    if name.startswith('Bras') and name.endswith('lia'):
        return 'Brasilia'
    return name


def load():
    df = pd.read_csv('Dataset.csv')
    df['City'] = df['City'].apply(fix_city)
    bad_zero = (df['Latitude'] == 0) | (df['Longitude'] == 0)
    bad_test = (df['Restaurant Name'].str.contains('Test Restaruants', case=False, na=False)
                & (df['City'] == 'New Delhi') & (df['Latitude'] == 35.0))
    df['coord_valid'] = ~(bad_zero | bad_test)
    dfc = df.dropna(subset=['Cuisines']).copy()
    dfc['rated'] = dfc['Aggregate rating'] > 0
    dfc['table'] = dfc['Has Table booking'] == 'Yes'
    dfc['delivery'] = dfc['Has Online delivery'] == 'Yes'
    return df, dfc


def summarise_city(dfc, name, min_locality=20):
    key = {c.lower(): c for c in dfc['City'].unique()}.get(name.strip().lower())
    if key is None:
        return f"City '{name}' not found."
    s = dfc[dfc['City'] == key]
    out = [f"{key}: {len(s)} restaurants (country code {s['Country Code'].iloc[0]})"]
    if len(s) < 20:
        out.append("Warning: fewer than 20 restaurants, so statistics are unreliable.")
    elif key not in NCR:
        out.append("Note: outside Delhi NCR this looks like a sample of about 20, "
                   "so counts do not show real density.")
    rated = s[s['rated']]
    out.append(f"Rated restaurants: {len(rated)} (unrated share {1 - s['rated'].mean():.2f})")
    out.append(f"Average rating (rated only): {rated['Aggregate rating'].mean():.2f}"
               if len(rated) else "No rated restaurants.")
    out.append("Price tier mix: " + ", ".join(
        f"tier {k}: {v:.0%}" for k, v in
        s['Price range'].value_counts(normalize=True).sort_index().items()))
    out.append(f"Online delivery: {s['delivery'].mean():.0%} | Table booking: {s['table'].mean():.0%}")
    cu = Counter(x.strip() for t in s['Cuisines'] for x in t.split(','))
    out.append("Top cuisines: " + ", ".join(f"{k} ({n})" for k, n in cu.most_common(5)))
    loc = s['Locality'].value_counts()
    big = loc[loc >= min_locality]
    if len(big):
        out.append("Largest localities: " + ", ".join(f"{k} ({n})" for k, n in big.head(5).items()))
    return "\n".join(out)


if __name__ == "__main__":
    df, dfc = load()
    print(f"Loaded {len(df)} restaurants; {int((~df['coord_valid']).sum())} have invalid coordinates "
          f"(excluded from maps only).")
    print("Type a city name (or press Enter to quit).")
    while True:
        city = input("City: ").strip()
        if not city:
            break
        print(summarise_city(dfc, city))
        print()
