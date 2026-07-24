-- ai used when needed to identify bugs and troubleshoot code

--to reset db, use cascade to drop dependencies
DROP TABLE IF EXISTS BusinessCategory CASCADE;
DROP TABLE IF EXISTS Review CASCADE;
DROP TABLE IF EXISTS CheckIn CASCADE;
DROP TABLE IF EXISTS Business CASCADE;
DROP TABLE IF EXISTS Category CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS Address CASCADE;
DROP TABLE IF EXISTS Zipcode CASCADE;

--create tables in order of dependencies, follows the er model 

CREATE TABLE Zipcode (
    zipcode VARCHAR(5) PRIMARY KEY,
    population INT NOT NULL,
    averageIncome NUMERIC(10,2) NOT NULL,
    businessCount INT NOT NULL DEFAULT 0
);

create table Address(
    addressID SERIAL PRIMARY KEY, --creates a unique id to use as primary key
    street VARCHAR(255) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(2) NOT NULL, -- US state abbrev. 
    zipcode VARCHAR(5) NOT NULL,
    FOREIGN KEY (zipcode) REFERENCES Zipcode(zipcode)
);

create table Business (
    businessID VARCHAR(22) PRIMARY KEY,
    name varchar(255) NOT NULL,
    stars NUMERIC(2,1) NOT NULL,
    reviewCount INT DEFAULT 0,
    totalCheckins INT DEFAULT 0, --calculated from each checkin
    averageReviewRating NUMERIC(2,1) DEFAULT 0.0, --calculated from each review

    --add popularity and success metrics for ms3
    popularityStatus BOOLEAN DEFAULT FALSE, --calculated from checkins and reviews
    successStatus BOOLEAN DEFAULT FALSE, --calculated from popularity and average review rating

    addressID INT NOT NULL, --derived from address

    FOREIGN KEY (addressID) REFERENCES Address(addressID)
); 

create table "user" ( --not on er diagram, but needed for reviews
    userID VARCHAR(22) PRIMARY KEY,
    reviewCount INT DEFAULT 0
);

create table Review (
    reviewID VARCHAR(22) PRIMARY KEY,
    userID VARCHAR(22) NOT NULL,
    stars NUMERIC(2,1) NOT NULL,
    businessID VARCHAR(22) NOT NULL,

    FOREIGN KEY (businessID) REFERENCES Business(businessID),
    FOREIGN KEY (userID) REFERENCES "user"(userID)
);


create table Category(
    categoryTitle VARCHAR(255) PRIMARY KEY
);

create table BusinessCategory (
    businessID VARCHAR(22) NOT NULL,
    categoryTitle VARCHAR(255) NOT NULL,
    PRIMARY KEY (businessID, categoryTitle),
    FOREIGN KEY (businessID) REFERENCES Business(businessID),
    FOREIGN KEY (categoryTitle) REFERENCES Category(categoryTitle)
);

CREATE TABLE CheckIn (
    businessID VARCHAR(22) NOT NULL,
    day VARCHAR(9) NOT NULL,  
    time VARCHAR(5) NOT NULL, 
    frequency INT NOT NULL,
    PRIMARY KEY (businessID, day, time), --weak entity so use composite for primary key
    FOREIGN KEY (businessID) REFERENCES Business(businessID)
);

---- query to determine if a business is popular, follows classificationMetrics.pdf

SELECT businessID, totalCheckins, reviewCount,
    CASE 
        WHEN totalCheckins > 100 AND reviewCount > 50 THEN TRUE
        ELSE FALSE
    END AS popularityStatus
FROM Business;

--- query to determine if a business is successful (just add on avg rating)
SELECT popularityStatus, averageReviewRating,
    CASE 
        WHEN popularityStatus = 'Popular' AND averageReviewRating >= 4.0 THEN TRUE
        ELSE FALSE
    END AS successStatus
FROM Business;