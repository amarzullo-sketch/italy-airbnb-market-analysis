- Italy Airbnb Market Investment Analysis
-- SQL analysis queries using cleaned Airbnb summary data

-- 1. Compare Rome, Florence, and Milan
SELECT
    city,
    total_listings,
    ROUND(avg_price, 2) AS avg_price,
    ROUND(avg_estimated_annual_revenue, 2) AS avg_estimated_revenue,
    ROUND(avg_recent_reviews, 2) AS avg_recent_reviews,
    ROUND(avg_rating, 2) AS avg_rating
FROM italy_airbnb_city_summary
ORDER BY avg_estimated_annual_revenue DESC;


-- 2. Top neighborhoods by market opportunity score
SELECT
    city,
    neighborhood,
    total_listings,
    ROUND(avg_price, 2) AS avg_price,
    ROUND(avg_estimated_annual_revenue, 2) AS avg_estimated_revenue,
    ROUND(avg_recent_reviews, 2) AS avg_recent_reviews,
    ROUND(avg_rating, 2) AS avg_rating,
    ROUND(market_opportunity_score, 2) AS market_opportunity_score
FROM italy_airbnb_neighborhood_summary
ORDER BY market_opportunity_score DESC
LIMIT 15;


-- 3. Top neighborhoods by average price
SELECT
    city,
    neighborhood,
    total_listings,
    ROUND(avg_price, 2) AS avg_price
FROM italy_airbnb_neighborhood_summary
WHERE total_listings >= 20
ORDER BY avg_price DESC
LIMIT 15;


-- 4. Top neighborhoods by estimated revenue
SELECT
    city,
    neighborhood,
    total_listings,
    ROUND(avg_estimated_annual_revenue, 2) AS avg_estimated_revenue
FROM italy_airbnb_neighborhood_summary
WHERE total_listings >= 20
ORDER BY avg_estimated_annual_revenue DESC
LIMIT 15;


-- 5. Top neighborhoods by recent demand
SELECT
    city,
    neighborhood,
    total_listings,
    ROUND(avg_recent_reviews, 2) AS avg_recent_reviews
FROM italy_airbnb_neighborhood_summary
WHERE total_listings >= 20
ORDER BY avg_recent_reviews DESC
LIMIT 15;


-- 6. Best balanced neighborhoods
SELECT
    city,
    neighborhood,
    total_listings,
    ROUND(avg_price, 2) AS avg_price,
    ROUND(avg_recent_reviews, 2) AS avg_recent_reviews,
    ROUND(avg_rating, 2) AS avg_rating,
    ROUND(market_opportunity_score, 2) AS market_opportunity_score
FROM italy_airbnb_neighborhood_summary
WHERE total_listings >= 20
  AND avg_rating >= 4.5
ORDER BY market_opportunity_score DESC
LIMIT 10;