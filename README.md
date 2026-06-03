# Italy Airbnb Market Investment Analysis

## Live Dashboard

[View the Tableau Public Dashboard](https://public.tableau.com/app/profile/alessandro.marzullo/viz/ItalyAirbnbMarketInvestmentAnalysis/ItalyAirbnbMarketInvestmentAnalysis)

## Results Summary

- Florence had the highest average nightly price.
- Milan showed strong estimated revenue potential in several neighborhoods.
- Rome had strong guest ratings but higher competition in some areas

## Project Overview

This project analyzes Airbnb market opportunity across three major Italian cities: **Rome, Florence, and Milan**. The goal was to compare city-level performance and identify neighborhoods that may offer stronger short-term rental potential based on pricing, estimated revenue, guest activity, listing competition, and guest satisfaction.

The project combines Python data cleaning, SQL-style analysis, and Tableau dashboarding to turn raw Airbnb listing data into a more useful market analysis.

## Business Question

Which Italian cities and neighborhoods show the strongest Airbnb market opportunity based on price, demand signals, estimated annual revenue, ratings, and competition?

## Cities Analyzed

* Rome
* Florence
* Milan

## Tools Used

* **Python** for data cleaning and feature engineering
* **Pandas** for working with large CSV files
* **SQL** for analysis queries and business question exploration
* **Tableau Public** for interactive dashboards and visual storytelling
* **GitHub** for project organization and version control

## Data Source

The data comes from **Inside Airbnb**, which provides publicly available Airbnb listing data for cities around the world.

This project uses listing-level data for Rome, Florence, and Milan. The raw data was cleaned and combined into one standardized dataset before being summarized at the city and neighborhood levels.

Because the data is based on a snapshot, the results should be interpreted as directional market estimates rather than exact financial outcomes.

## Key Metrics

The project focuses on the following metrics:

* **Average Nightly Price**
  Average listed nightly price for Airbnb listings.

* **Availability Rate**
  Share of days a listing is available during the year.

* **Occupancy Proxy**
  Estimated occupancy based on availability data. Since unavailable nights can mean either booked nights or host-blocked nights, this is treated as a proxy rather than confirmed occupancy.

* **Estimated Annual Revenue**
  An annualized revenue estimate based on nightly price and estimated booked nights.

* **Recent Reviews**
  Recent review activity used as a demand signal.

* **Average Guest Rating**
  Average review score across listings.

* **Total Listings**
  Number of active listings in a city or neighborhood.

* **Market Opportunity Score**
  A custom score combining revenue potential, demand, rating strength, pricing, and competition indicators.

## Methodology

### 1. Data Collection

I downloaded Airbnb listing data for Rome, Florence, and Milan. Each city had its own listing file, and the files were placed into a structured project folder before cleaning.

### 2. Data Cleaning with Python

The Python script cleaned and combined the city datasets into one standardized file. The cleaning process included:

* Loading the listing files for all three cities
* Adding a city column to each dataset
* Combining the cities into one dataset
* Cleaning price fields
* Removing unusable or incomplete records
* Converting key columns into numeric formats
* Creating additional calculated metrics
* Exporting cleaned datasets for Tableau and SQL analysis

The main cleaned output files are:

* `italy_airbnb_listings_cleaned.csv`
* `italy_airbnb_city_summary.csv`
* `italy_airbnb_neighborhood_summary.csv`

### 3. Feature Engineering

Several new variables were created to make the dataset more useful for market analysis.

Examples include:

* `availability_rate`
* `occupancy_proxy`
* `estimated_booked_nights`
* `estimated_annual_revenue`
* `price_per_guest`
* `market_opportunity_score`

These features helped move the project beyond simple descriptive statistics and toward a more practical investment-style analysis.

### 4. City-Level Analysis

The city summary file was used to compare Rome, Florence, and Milan across:

* Average nightly price
* Estimated annual revenue
* Recent review activity
* Average guest rating
* Total listing volume

This gave a high-level view of how each city performs overall.

### 5. Neighborhood-Level Analysis

The neighborhood summary file was used to identify stronger and weaker areas within each city.

Neighborhoods were compared by:

* Market opportunity score
* Estimated annual revenue
* Recent reviews
* Listing competition
* Average price
* Average rating

This was important because city-level averages can hide major differences between neighborhoods.

### 6. Tableau Dashboard Development

The final dashboard was built in Tableau Public as an interactive story with three sections:

1. **Executive Overview**
2. **Neighborhood Opportunity**
3. **Market Map**

The dashboard allows users to compare cities, explore neighborhood rankings, and view Airbnb listings geographically.

## Dashboard Pages

### Executive Overview

The Executive Overview compares Rome, Florence, and Milan using city-level metrics.

It includes:

* Estimated annual revenue by city
* Average nightly price by city
* Recent reviews by city
* Average guest rating by city


### Neighborhood Opportunity

The Neighborhood Opportunity page ranks neighborhoods based on market opportunity, estimated revenue, demand, and competition.

It includes:

* Top neighborhoods by opportunity score
* Neighborhood listing competition
* Top neighborhoods by estimated revenue
* Top neighborhoods by demand


### Market Map

The Market Map shows individual Airbnb listings by location. It allows filtering by city, room type, price, and neighborhood.

## Key Findings

### Florence had the highest average nightly price

Florence showed the highest average nightly price among the three cities. This suggests that listings in Florence may command stronger nightly rates, likely due to the city’s tourism demand and smaller geographic market.

### Milan showed strong revenue potential in several neighborhoods

Milan had multiple neighborhoods ranking highly by estimated annual revenue and market opportunity score. This suggests that Milan may have strong short-term rental potential in specific neighborhoods, even if its average nightly price was not the highest overall.

### Rome had strong ratings but higher competition in some areas

Rome performed well in guest ratings, but some neighborhoods had much higher listing competition. This makes neighborhood selection especially important when evaluating Rome.

### Neighborhood-level analysis was more useful than city-level averages

The city-level comparison was useful for a broad market overview, but the neighborhood-level analysis provided more practical insight. Some neighborhoods performed much better than their city averages, while others were more crowded or less attractive based on the opportunity score.

## Limitations

This project uses publicly available Airbnb snapshot data, so the analysis has several limitations.

First, Airbnb calendar availability does not clearly separate booked nights from host-blocked nights. Because of that, the occupancy proxy and estimated annual revenue should not be interpreted as exact booking or revenue numbers.

Second, the analysis does not include operating costs, cleaning fees, taxes, local regulations, seasonality, or property acquisition costs. Those would be necessary for a complete investment decision.

Third, the market opportunity score is a custom scoring method. It is useful for comparison, but it should be treated as a ranking tool rather than a definitive investment recommendation.

## Project Structure

```text
italy-airbnb-market-analysis/
│
├── clean_airbnb_data.py
├── README.md
├── .gitignore
│
├── data/
│   └── cleaned/
│       ├── italy_airbnb_city_summary.csv
│       ├── italy_airbnb_listings_cleaned.csv
│       └── italy_airbnb_neighborhood_summary.csv
│
├── sql/
│   └── analysis_queries.sql
│
├── tableau/
│   └── italy_airbnb_market_analysis.twbx

```

## Files Included

### `clean_airbnb_data.py`

Python script used to clean, combine, and transform the Airbnb data.

### `data/cleaned/`

Folder containing the cleaned CSV files used for analysis and dashboarding.

### `sql/analysis_queries.sql`

SQL queries written to explore city and neighborhood performance.

### `tableau/`

Folder containing the Tableau workbook.

## How to Run the Project

1. Clone the repository.

```bash
git clone https://github.com/amarzullo-sketch/italy-airbnb-market-analysis.git
```

2. Open the project folder.

```bash
cd italy-airbnb-market-analysis
```

3. Install required Python packages.

```bash
pip install pandas
```

4. Run the cleaning script.

```bash
python clean_airbnb_data.py
```

5. Open the Tableau Public dashboard using the live link above.

## Skills Demonstrated

This project demonstrates:

* Data cleaning with Python
* Working with large CSV files
* Feature engineering
* City-level and neighborhood-level analysis
* SQL analysis
* Data visualization in Tableau
* Dashboard design
* Business-oriented data storytelling
* GitHub project organization

## Final Takeaway

The analysis suggests that Airbnb market opportunity varies significantly by neighborhood, not just by city. Florence had the strongest average nightly pricing, Milan showed strong estimated revenue potential in several neighborhoods, and Rome had strong guest ratings but higher competition in some areas.

The main takeaway is that a strong Airbnb market analysis should look beyond city averages and focus on neighborhood-level performance, demand signals, and competition.
