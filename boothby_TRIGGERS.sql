-- script to update business stats if new data inserted

CREATE OR REPLACE FUNCTION updateBusinessReviewStats()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Business
    SET reviewCount = (SELECT COUNT(*) FROM Review WHERE Review.businessID = NEW.businessID), --increment review count
        averageReviewRating = (SELECT AVG(stars) FROM Review WHERE Review.businessID = NEW.businessID) --update average review rating
    WHERE businessID = NEW.businessID;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql; 

CREATE TRIGGER updateBusinessReviewStatsTrigger
AFTER INSERT ON Review
FOR EACH ROW
EXECUTE FUNCTION updateBusinessReviewStats();

--below is commands used to test: 
/* 
SELECT userid FROM "user" LIMIT 1;
SELECT businessid, reviewcount, averagereviewrating FROM business LIMIT 1;

INSERT INTO review (reviewid, userid, stars, businessid)
VALUES ('trigger_test', 'om5ZiponkpRqUNa3pVPiRg', 5.0, '5HwBX7gq2a3HkbPusIkypg');

DELETE FROM review WHERE reviewid = 'trigger_test'; --reset changes, in review table only */