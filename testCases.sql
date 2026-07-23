--this file contains the sql commands to test if zipcode and popularity/success metrics work as intended
--meant to copy/paste in terminal, not run whole script

--test to see num items in each table
SELECT 'zipcode' AS tbl, COUNT(*) FROM zipcode
UNION ALL SELECT 'address', COUNT(*) FROM address
UNION ALL SELECT 'business', COUNT(*) FROM business
UNION ALL SELECT 'user', COUNT(*) FROM "user"
UNION ALL SELECT 'review', COUNT(*) FROM review
UNION ALL SELECT 'category', COUNT(*) FROM category
UNION ALL SELECT 'businesscategory', COUNT(*) FROM businesscategory
UNION ALL SELECT 'checkin', COUNT(*) FROM checkin;

--check sample of zipcode data (top 10)
SELECT zipcode, businesscount FROM zipcode ORDER BY businesscount DESC LIMIT 10;

--check num popular 
SELECT
    CASE 
        WHEN totalcheckins > 1000 AND reviewcount > 100 THEN 'Popular'
        ELSE 'Not Popular'
    END AS popularitystatus,
    COUNT(*) AS num_businesses
FROM business
GROUP BY
    CASE 
        WHEN totalcheckins > 1000 AND reviewcount > 100 THEN 'Popular'
        ELSE 'Not Popular'
    END;

--check num successful
SELECT
    CASE 
        WHEN totalcheckins > 1000 AND reviewcount > 100 AND averagereviewrating >= 4.0 THEN 'Successful'
        ELSE 'Not Successful'
    END AS successstatus,
    COUNT(*) AS num_businesses
FROM business
GROUP BY successstatus;