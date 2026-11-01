# Location-Based Analysis

## Title and Purpose

* **Location-Based Analysis:** A geographical study of the company's `Dataset.csv`, which contains 9551 restaurants and 21 columns.
* **Author:** Niharika Gupta.

## Folder Contents

* `location_analysis.ipynb`: The complete analysis workflow with outputs, including coordinate validation, maps, concentration analysis, city and locality statistics, insights, and charts.
* `location_analysis.py`: A standalone script that generates a profile for any city entered by the user. It requires only pandas and `Dataset.csv`.
* `Dataset.csv`: The original dataset, preserved without modifications.
* `restaurant_map.html`: A self-contained Plotly map showing the 7549 Delhi NCR points, with interactive hover details. The map works offline, but street backgrounds are unavailable because the free OpenStreetMap and CartoDB tile services blocked access.

## How to Run

* **Notebook:** Upload `Dataset.csv` to Google Colab, then select Runtime → Run all.
* **Script:** Install pandas, place `location_analysis.py` and `Dataset.csv` in the same folder, and execute:

```
python location_analysis.py
```

Enter a city name to view its profile. To exit, press Enter on an empty line.

## Approach

* **Coordinate validation:** Corrected 3 corrupted city names (Istanbul, Sao Paulo, Brasilia). A total of 499 restaurants have a zero latitude or longitude, including 497 with both coordinates set to zero. One test entry is approximately 4268 km from its city. Consequently, 500 records are flagged as invalid, leaving 9051 usable map points. These records are excluded from maps only.
* **Maps:** Generated global, India (8155 valid points), and Delhi NCR (7549 points) views, along with an interactive NCR map.
* **Geographical concentration:** India accounts for 90.6% of restaurants, while New Delhi alone represents 57.3% (5473). The four NCR cities together account for 82.9% (7922). The city-level Gini is 0.878, and the NCR locality Gini is 0.621.
* **Statistical analysis:** Ratings are calculated using rated restaurants only, since a rating of 0 means the restaurant is not rated. Price range is used instead of cost because currency labels are unreliable.
* **Locality specialties and insights:** Locality specialties are identified using lift, with a minimum of 8 restaurants. Insights are evaluated using Spearman correlations and chi-square tests.

## Key Findings

* Across 97 NCR localities, average price is associated with average rating (rho 0.64), median votes (0.78), table-booking share (0.84), and unrated share (-0.72).
* Delivery and table-booking rates vary across the four major NCR cities. Delivery ranges from 38.0% in Gurgaon to 13.9% in Faridabad, while table booking ranges from 18.2% to 6.0%.
* Lower ratings in cheaper areas may partly be explained by missing ratings. The analysis does not establish that these areas have lower restaurant quality.

## Limitations

* Cities outside NCR appear to contain fixed samples of approximately 20 restaurants, with 67 cities having exactly 20 entries. Their restaurant counts do not represent actual geographical densities, and their ratings should not be directly compared with NCR.
* Some names and addresses contain corrupted characters inherited from the source file, and some coordinates appear rounded.
* Correlations describe associations between locality-level averages; they do not establish causal relationships.

## Example Run

```
Loaded 9551 restaurants; 500 have invalid coordinates (excluded from maps only).
Type a city name (or press Enter to quit).
City: Gurgaon
Gurgaon: 1118 restaurants (country code 1)
Rated restaurants: 890 (unrated share 0.20)
Average rating (rated only): 3.33
Price tier mix: tier 1: 41%, tier 2: 39%, tier 3: 14%, tier 4: 6%
Online delivery: 38% | Table booking: 18%
Top cuisines: North Indian (508), Chinese (324), Fast Food (220), Mughlai (117), Bakery (110)
Largest localities: DLF Phase 3 (69), Sector 56 (54), Sector 14 (52), Palam Vihar (49), Sohna Road (42)
```