--run w: psql -U sydnee -d yelpdb -f boothby_UPDATE.sql

--first store total checkins for each business, store in temp for now
CREATE TEMP TABLE checkin_stats AS
SELECT businessID, SUM(frequency) AS total_checkins
FROM Checkin
GROUP BY businessID;

UPDATE business b --update business totals where id matches temp
SET totalCheckins = cs.total_checkins --my table uses totalCheckins name 
FROM checkin_stats cs
WHERE b.businessID = cs.businessID;


-- review count, similar logic to total checkins
CREATE TEMP TABLE reviewcount_stats AS
SELECT businessID, COUNT(*) AS review_count 
FROM Review
GROUP BY businessID;

UPDATE business b --update table where id matches
SET reviewCount = rc.review_count
FROM reviewcount_stats rc
WHERE b.businessID = rc.businessID;

--determine avverage review rating for each business
CREATE TEMP TABLE reviewrating_stats AS
SELECT businessID, AVG(stars) AS avg_review_rating --take average of stars for each busid
FROM Review
GROUP BY businessID;

UPDATE business b
SET averageReviewRating = rr.avg_review_rating
FROM reviewrating_stats rr
WHERE b.businessID = rr.businessID;

